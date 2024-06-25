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
    scene.add(new THREE.HemisphereLight(0xffffff, 0.5));
    var ambientLight = new THREE.AmbientLight('#555');
    scene.add(ambientLight);

    const geometry = new THREE.BoxGeometry();
    const material = new THREE.MeshStandardMaterial({
        roughness: 0.2,  // Low roughness for glossiness
        metalness: 0.6,  // Some metalness for reflective quality
    });
    const cube = new THREE.Mesh(geometry, material);
    scene.add(cube);
      
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
