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
  

    // Create a cube with wooden texture and glossy effect
    const geometry = new THREE.BoxGeometry();
    const material = new THREE.MeshStandardMaterial({
        map: woodTexture,
        roughness: 0.2,  // Low roughness for glossiness
        metalness: 0.6,  // Some metalness for reflective quality
    });
    const cube = new THREE.Mesh(geometry, material);
    scene.add(cube);

    // Position the camera
    camera.position.z = 5;

    // Add ambient light
    const ambientLight = new THREE.AmbientLight(0x404040); // Soft white light
    scene.add(ambientLight);

    // Add spotlight for product showcase effect
    const spotLight = new THREE.SpotLight(0xffffff);
    spotLight.position.set(5, 5, 5);
    spotLight.castShadow = true;
    spotLight.angle = Math.PI / 6;
    spotLight.penumbra = 0.1;
    spotLight.decay = 2;
    spotLight.distance = 200;
    scene.add(spotLight);

    // Add a point light for extra illumination
    const pointLight = new THREE.PointLight(0xffffff, 1, 100);
    pointLight.position.set(-5, -5, -5);
    scene.add(pointLight);
  }

  disconnectedCallback() {
    this.connected = false;
  }
}

customElements.define('stl-viewer', STLViewer);