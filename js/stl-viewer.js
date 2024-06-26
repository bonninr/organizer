//import './three.min.js';
//import './STLLoader.js';
//import './OrbitControls.js';

class STLViewer extends HTMLElement {
  constructor() {
    super();
  }

  connectedCallback() {
    this.connected = true;

    const shadowRoot = this.attachShadow({ mode: 'open' });
    const container = document.createElement('div');
    container.style.width = '100%';
    container.style.height = '100%';

    shadowRoot.appendChild(container);

    if (!this.hasAttribute('model')) {
      throw new Error('model attribute is required');
    }

    const model = this.getAttribute('model');

    let camera = new THREE.PerspectiveCamera(100, container.clientWidth / container.clientHeight, 300, 2800);
    
    let renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(container.clientWidth, container.clientHeight);
    container.appendChild(renderer.domElement);

    window.addEventListener('resize', function () {
      renderer.setSize(container.clientWidth, container.clientHeight);
      camera.aspect = container.clientWidth / container.clientHeight;
      camera.updateProjectionMatrix();
    }, false);
    let controls = new THREE.OrbitControls(camera, renderer.domElement);
    controls.enableZoom = true;
    let scene = new THREE.Scene();


    console.log("made it this far");

    new THREE.STLLoader().load(model, (geometry) => {
      let  material = new THREE.MeshPhysicalMaterial({
        roughness: 0,
        transmission: 0.5,
        clearcoat: 1
      });
      let mesh = new THREE.Mesh(geometry, material);
      mesh.castShadow = true
      mesh.receiveShadow = true
      mesh.rotation.x = Math.PI *1.5  ;
      //scene.add(mesh);
  
      const woodtextureLoader = new THREE.TextureLoader();
      const woodTexture = woodtextureLoader.load('https://raw.githubusercontent.com/sanches812/ash-wood-textures/main/Ash-Wood-Seamless-Texture-7.jpg'); // Replace with your texture URL

      const geometry2 = new THREE.BoxGeometry(1000,1000,1000);
      const material2 = new THREE.MeshPhysicalMaterial({
        map: woodTexture,

        roughness: 0.2,
        transmission: 0.5,
        clearcoat: 1,
        
      });
      const cube = new THREE.Mesh(geometry2, material2);
      scene.add(cube);


      const ambientLight = new THREE.AmbientLight(0x404040, 0.3); // soft white light
      scene.add(ambientLight);
  
      const keyLight = new THREE.DirectionalLight(0xffffff,  0.7);
      keyLight.position.set(-100, 100, 100);
      scene.add(keyLight);

  
      const fillLight = new THREE.DirectionalLight(0xffffff, 0.75);
      fillLight.position.set(100, 100, 100);
      scene.add(fillLight);
  

      
      const backLight = new THREE.DirectionalLight(0xffffff, 0.7);
      backLight.position.set(0, 10, -100);
      scene.add(backLight);

      const loader = new THREE.TextureLoader();
      loader.load('https://images.pexels.com/photos/11421550/pexels-photo-11421550.jpeg' , function(texture)
            {
             scene.background = texture;  
            });

      var geo = new THREE.PlaneBufferGeometry(800, 1500, 8, 8);
      var mat = new THREE.MeshBasicMaterial({ color: 0x000000, side: THREE.DoubleSide });
      var plane = new THREE.Mesh(geo, mat);
      plane.rotateX( - Math.PI / 2);
      plane.position.y -= 600;

      scene.add(plane);


      let middle = new THREE.Vector3();
      geometry.computeBoundingBox();
      geometry.boundingBox.getCenter(middle);
      mesh.geometry.applyMatrix4(new THREE.Matrix4().makeTranslation(-middle.x, -middle.y, -middle.z));
      let largestDimension = Math.max(geometry.boundingBox.max.x, geometry.boundingBox.max.y, geometry.boundingBox.max.z)
      camera.position.z = largestDimension * 1.8;
      camera.position.y = 20;
      camera.position.x = 30;

      controls.autoRotate = true;
      controls.autoRotateSpeed = 2;
      let animate = () => {
        controls.update();
        renderer.render(scene, camera);
        if (this.connected) {
          requestAnimationFrame(animate);
        }
      };
      animate();
    });
  }

  disconnectedCallback() {
    this.connected = false;
  }
}

customElements.define('stl-viewer', STLViewer);