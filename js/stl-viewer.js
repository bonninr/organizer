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
    scene.add(new THREE.HemisphereLight(0xffffff, 1.5));

    const textureLoader = new THREE.TextureLoader();
    const woodTexture = textureLoader.load('https://images.pexels.com/photos/11421550/pexels-photo-11421550.jpeg')
    const geometry = new THREE.BoxGeometry();
    const material = new THREE.MeshStandardMaterial({
      map: woodTexture,
      roughness: 0.2,  // Low roughness for glossiness
      metalness: 0.6,  // Some metalness for reflective quality
    });
    const cube = new THREE.Mesh(geometry, material);
    scene.add(cube);
  
    var ambientLight = new THREE.AmbientLight('#555');
    scene.add(ambientLight);

    var geo = new THREE.PlaneBufferGeometry(800, 1500, 8, 8);
    var mat = new THREE.MeshBasicMaterial({ color: 0x000000, side: THREE.DoubleSide });
    var plane = new THREE.Mesh(geo, mat);
    plane.rotateX( - Math.PI / 2);
    plane.position.y -= 600;

    scene.add(plane);

    let middle = new THREE.Vector3();
    geometry.computeBoundingBox();
    geometry.boundingBox.getCenter(middle);
    cube.geometry.applyMatrix4(new THREE.Matrix4().makeTranslation(-middle.x, -middle.y, -middle.z));
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
  }

  disconnectedCallback() {
    this.connected = false;
  }
}

customElements.define('stl-viewer', STLViewer);
