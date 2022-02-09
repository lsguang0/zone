<template>
<!-- <div id="game"></div> -->
</template>
<script setup >
import { onBeforeUnmount, onMounted, onUnmounted } from 'vue';
import * as THREE from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
import { Octree } from 'three/examples/jsm/math/Octree.js';
import { Capsule } from 'three/examples/jsm/math/Capsule.js';


const app = {
    scene: new THREE.Scene(),
    camera: new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 100),
    renderer: new THREE.WebGLRenderer({antialias: true}),
    control: null
}


const worldOctree = new Octree();

const clock = new THREE.Clock();
const playerCollider = new Capsule( new THREE.Vector3( 0, 0.35, 0 ), new THREE.Vector3( 0, 1, 0 ), 0.35 );
const playerVelocity = new THREE.Vector3();
const playerDirection = new THREE.Vector3();

const GRAVITY = 30;

const NUM_SPHERES = 100;
// 球体半径
const SPHERE_RADIUS = 0.2;
const STEPS_PER_FRAME = 5;

let playerOnFloor = false;

const keyStates = {};

const spheres = [];
let sphereIdx = 0;
let mouseTime = 0;

const vector1 = new THREE.Vector3();
const vector2 = new THREE.Vector3();
const vector3 = new THREE.Vector3();

function animate () {
    const deltaTime = Math.min( 0.05, clock.getDelta() ) / STEPS_PER_FRAME;
    for ( let i = 0; i < STEPS_PER_FRAME; i ++ ) {

        controls( deltaTime );

        updatePlayer( deltaTime );

        updateSpheres( deltaTime );

    }
    const {scene, camera, renderer, control} = app;
    // control.update()
    renderer.render(scene, camera);
    requestAnimationFrame(animate)

}
function getForwardVector() {
    const { camera } = app;
    camera.getWorldDirection( playerDirection );
    playerDirection.y = 0;
    playerDirection.normalize();
    return playerDirection;
}
function getSideVector() {
    const {camera} = app;
    camera.getWorldDirection( playerDirection );
    playerDirection.y = 0;
    playerDirection.normalize();
    playerDirection.cross( camera.up );

    return playerDirection;

}
function controls(deltaTime) {

    const speedDelta = deltaTime * ( playerOnFloor ? 25 : 8 );

    if ( keyStates[ 'KeyW' ] ) {

        playerVelocity.add( getForwardVector().multiplyScalar( speedDelta ) );

    }

    if ( keyStates[ 'KeyS' ] ) {

        playerVelocity.add( getForwardVector().multiplyScalar( - speedDelta ) );

    }

    if ( keyStates[ 'KeyA' ] ) {

        playerVelocity.add( getSideVector().multiplyScalar( - speedDelta ) );

    }

    if ( keyStates[ 'KeyD' ] ) {

        playerVelocity.add( getSideVector().multiplyScalar( speedDelta ) );

    }

    if ( playerOnFloor ) {

        if ( keyStates[ 'Space' ] ) {

            playerVelocity.y = 15;

        }

    }
}
function updatePlayer(deltaTime) {
    const { camera } = app;
    let damping = Math.exp( - 4 * deltaTime ) - 1;

    if ( ! playerOnFloor ) {

        playerVelocity.y -= GRAVITY * deltaTime;

        // small air resistance
        damping *= 0.1;

    }

    playerVelocity.addScaledVector( playerVelocity, damping );

    const deltaPosition = playerVelocity.clone().multiplyScalar( deltaTime );
    playerCollider.translate( deltaPosition );

    playerCollisions();

    camera.position.copy( playerCollider.end );

}
function playerCollisions() {

    const result = worldOctree.capsuleIntersect( playerCollider );
    playerOnFloor = false;

    if ( result ) {

        playerOnFloor = result.normal.y > 0;

        if ( ! playerOnFloor ) {

            playerVelocity.addScaledVector( result.normal, - result.normal.dot( playerVelocity ) );

        }

        playerCollider.translate( result.normal.multiplyScalar( result.depth ) );

    }

}

function updateSpheres( deltaTime ) {

    spheres.forEach( sphere => {

        sphere.collider.center.addScaledVector( sphere.velocity, deltaTime );

        const result = worldOctree.sphereIntersect( sphere.collider );

        if ( result ) {

            sphere.velocity.addScaledVector( result.normal, - result.normal.dot( sphere.velocity ) * 1.5 );
            sphere.collider.center.add( result.normal.multiplyScalar( result.depth ) );

        } else {

            sphere.velocity.y -= GRAVITY * deltaTime;

        }

        const damping = Math.exp( - 1.5 * deltaTime ) - 1;
        sphere.velocity.addScaledVector( sphere.velocity, damping );

        playerSphereCollision( sphere );

    } );

    spheresCollisions();

    for ( const sphere of spheres ) {

        sphere.mesh.position.copy( sphere.collider.center );

    }

}
function playerSphereCollision( sphere ) {

    const center = vector1.addVectors( playerCollider.start, playerCollider.end ).multiplyScalar( 0.5 );

    const sphere_center = sphere.collider.center;

    const r = playerCollider.radius + sphere.collider.radius;
    const r2 = r * r;

    // approximation: player = 3 spheres

    for ( const point of [ playerCollider.start, playerCollider.end, center ] ) {

        const d2 = point.distanceToSquared( sphere_center );

        if ( d2 < r2 ) {

            const normal = vector1.subVectors( point, sphere_center ).normalize();
            const v1 = vector2.copy( normal ).multiplyScalar( normal.dot( playerVelocity ) );
            const v2 = vector3.copy( normal ).multiplyScalar( normal.dot( sphere.velocity ) );

            playerVelocity.add( v2 ).sub( v1 );
            sphere.velocity.add( v1 ).sub( v2 );

            const d = ( r - Math.sqrt( d2 ) ) / 2;
            sphere_center.addScaledVector( normal, - d );

        }

    }

}

function spheresCollisions() {

    for ( let i = 0, length = spheres.length; i < length; i ++ ) {

        const s1 = spheres[ i ];

        for ( let j = i + 1; j < length; j ++ ) {

            const s2 = spheres[ j ];

            const d2 = s1.collider.center.distanceToSquared( s2.collider.center );
            const r = s1.collider.radius + s2.collider.radius;
            const r2 = r * r;

            if ( d2 < r2 ) {

                const normal = vector1.subVectors( s1.collider.center, s2.collider.center ).normalize();
                const v1 = vector2.copy( normal ).multiplyScalar( normal.dot( s1.velocity ) );
                const v2 = vector3.copy( normal ).multiplyScalar( normal.dot( s2.velocity ) );

                s1.velocity.add( v2 ).sub( v1 );
                s2.velocity.add( v1 ).sub( v2 );

                const d = ( r - Math.sqrt( d2 ) ) / 2;

                s1.collider.center.addScaledVector( normal, d );
                s2.collider.center.addScaledVector( normal, - d );

            }

        }

    }

}
function initScene () {
    const {scene, renderer, camera} = app;

    app.scene.background = new THREE.Color( 0x88ccff );
    app.camera.rotation.order = 'YXZ';

    // app.control = new OrbitControls(app.camera, app.renderer.domElement);

    const ambientlight = new THREE.AmbientLight( 0x6688cc );
    app.scene.add( ambientlight );
    
    // const fillLight1 = new THREE.DirectionalLight( 0xff9999, 0.5 );
    // fillLight1.position.set( - 1, 1, 2 );
    // app.scene.add( fillLight1 );

    // const fillLight2 = new THREE.DirectionalLight( 0x8888ff, 0.2 );
    // fillLight2.position.set( 0, - 1, 0 );
    // app.scene.add( fillLight2 );
    
    const directionalLight = new THREE.DirectionalLight( 0xffffaa, 1.2 );
    directionalLight.position.set( - 5, 25, - 1 );
    // 阴影
    directionalLight.castShadow = true;
    // 使用OrthographicCamera计算阴影 DirectionalLightShadow
    directionalLight.shadow.camera.near = 0.01;
    directionalLight.shadow.camera.far = 500;
    directionalLight.shadow.camera.right = 30;
    directionalLight.shadow.camera.left = - 30;
    directionalLight.shadow.camera.top	= 30;
    directionalLight.shadow.camera.bottom = - 30;

    directionalLight.shadow.mapSize.width = 1024;
    directionalLight.shadow.mapSize.height = 1024;
    // 阴影属性
    directionalLight.shadow.radius = 4;
    directionalLight.shadow.bias = - 0.00006;
    scene.add( directionalLight );

    renderer.shadowMap.enabled = true;
    // 阴影处理类型 值为1\2\3\4
    renderer.shadowMap.type = THREE.VSMShadowMap;



    const sphereGeometry = new THREE.SphereGeometry( SPHERE_RADIUS, 32, 32 );
    // roughness 粗糙程度 metalness 材质与金属相似度
    const sphereMaterial = new THREE.MeshStandardMaterial( { color: 0x888855, roughness: 0.8, metalness: 0.5 } );


    for ( let i = 0; i < NUM_SPHERES; i ++ ) {

        const sphere = new THREE.Mesh( sphereGeometry, sphereMaterial );
        sphere.castShadow = true;
        sphere.receiveShadow = true;

        scene.add( sphere );

        spheres.push( { mesh: sphere, collider: new THREE.Sphere( new THREE.Vector3( 0, - 100, 0 ), SPHERE_RADIUS ), velocity: new THREE.Vector3() } );

    }

    document.addEventListener( 'keydown', ( event ) => {

        keyStates[ event.code ] = true;

    } );

    document.addEventListener( 'keyup', ( event ) => {

        keyStates[ event.code ] = false;

    } );

    document.addEventListener( 'mousedown', mousedownFunc);

    document.addEventListener( 'mouseup', throwBall);

    document.body.addEventListener( 'mousemove', mousemoveFunc);
    
    const loader = new GLTFLoader()
    loader.load('./glb/collision-world.glb', gltf => {
        scene.add(gltf.scene);
        worldOctree.fromGraphNode( gltf.scene );
        // 所有资源素设置阴影和优化贴图
        gltf.scene.traverse( child => {
            if ( child.isMesh ) {
                child.castShadow = true;
                child.receiveShadow = true;
                // 贴图的粗糙度
                if ( child.material.map ) {
                    child.material.map.anisotropy = 8;
                }
            }
        } );
        animate();
    })
}
function throwBall() {
    const {camera} = app;
    const sphere = spheres[ sphereIdx ];

    camera.getWorldDirection( playerDirection );

    sphere.collider.center.copy( playerCollider.end ).addScaledVector( playerDirection, playerCollider.radius * 1.5 );

    // throw the ball with more force if we hold the button longer, and if we move forward
    // math.exp e的x次方 参数为x  performance.now() 页面加载已完成时间
    const impulse = 15 + 30 * ( 1 - Math.exp( ( mouseTime - performance.now() ) * 0.001 ) );

    sphere.velocity.copy( playerDirection ).multiplyScalar( impulse );
    sphere.velocity.addScaledVector( playerVelocity, 2 );

    sphereIdx = ( sphereIdx + 1 ) % spheres.length;

}
function mousemoveFunc(event) {
    const {camera} = app;
    if ( document.pointerLockElement === document.body ) {
        camera.rotation.y -= event.movementX / 500;
        camera.rotation.x -= event.movementY / 500;
    }
}
function mousedownFunc() {
    // 将鼠标指针锁定在指定元素上
    document.body.requestPointerLock();
    mouseTime = performance.now();
}

onMounted(() => {
    const content = document.getElementById('app');
    if (content) {
        app.renderer.setSize(content.offsetWidth, content.offsetHeight);
        content.appendChild(app.renderer.domElement);
        // app.camera.position.z = 20;
    }
    initScene()
})

onBeforeUnmount(() => {
    document.removeEventListener('mousedown', mousedownFunc)
    document.removeEventListener('mouseup', throwBall)
    document.body.removeEventListener('mousemove', mousemoveFunc)
    document.exitPointerLock();
})

</script>
<style lang="scss">
// #game {
//     height: 100%;
//     width: 100%;
// }
</style>