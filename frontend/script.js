const courses = [
    { id: 'mechanics', title: 'Classical Mechanics' },
    { id: 'thermo', title: 'Thermodynamics' },
    { id: 'em', title: 'Electromagnetism' },
];

const problems = {
    mechanics: [
        { id: 'm1', title: 'Projectile Motion', description: 'An object is thrown with an initial velocity of $v_0$. Its height $h$ at time $t$ is given by the equation $h(t) = h_0 + v_0t - \\frac{1}{2}gt^2$. Find the maximum height.', solution: 'The maximum height of a projectile occurs at the peak of its trajectory. At this point, the vertical velocity is zero. Using the kinematic equation $v = v_0 - gt$, we set $v=0$ to find the time to reach maximum height: $t = \frac{v_0}{g}$. Substituting this time back into the height equation $h(t) = h_0 + v_0t - \\frac{1}{2}gt^2$, we get $h_{max} = h_0 + \\frac{v_0^2}{2g}$.' },
        { id: 'm2', title: 'Block on an Incline', description: 'A block of mass m is placed on a frictionless incline of angle theta. What is the acceleration of the block?', solution: 'For a block on a frictionless incline, the forces acting on the block are gravity ($mg$) and the normal force ($N$). We resolve the gravitational force into components parallel and perpendicular to the incline. The component parallel to the incline is $mg\sin(\theta)$, and the component perpendicular is $mg\cos(\theta)$. Since there is no friction, the net force along the incline is $mg\sin(\theta)$. By Newton\'s second law, $F_{net} = ma$, so $ma = mg\sin(\theta)$. Therefore, the acceleration of the block is $a = g\sin(\theta)$.' },
    ],
    thermo: [
        { id: 't1', title: 'Ideal Gas Law', description: 'An ideal gas is held in a container of volume V at temperature T. If the number of moles is n, what is the pressure?', solution: 'The Ideal Gas Law states $PV = nRT$, where $P$ is pressure, $V$ is volume, $n$ is the number of moles, $R$ is the ideal gas constant, and $T$ is temperature. Therefore, the pressure is $P = \frac{nRT}{V}$.' }
    ],
    em: [
        { id: 'e1', title: "Coulomb's Law", description: 'Two point charges, q1 and q2, are separated by a distance r. What is the force between them?', solution: 'Coulomb\'s Law describes the force between two point charges. The magnitude of the electrostatic force $F$ between two point charges $q_1$ and $q_2$ separated by a distance $r$ is given by $F = k\frac{|q_1q_2|}{r^2}$, where $k$ is Coulomb\'s constant ($k \approx 8.987 \times 10^9 \text{ N} \cdot \text{m}^2/\text{C}^2$). The force is attractive if the charges have opposite signs and repulsive if they have the same sign.' },
    ],
};


const mainContent = document.getElementById('main-content');
const homeButton = document.getElementById('home-button');


async function loadView(viewName, setupCallback) {
    // Load HTML
    const response = await fetch(`views/${viewName}/index.html`);
    const viewContent = await response.text();
    mainContent.innerHTML = viewContent;

    // Load CSS
    const oldLink = document.getElementById('view-style');
    if (oldLink) {
        oldLink.remove();
    }
    if (viewName !== 'about') { // No specific CSS for about page yet
        const link = document.createElement('link');
        link.id = 'view-style';
        link.rel = 'stylesheet';
        link.href = `views/${viewName}/style.css`;
        document.head.appendChild(link);
    }

    // Load JS
    const oldScript = document.getElementById('view-script');
    if (oldScript) {
        oldScript.remove();
    }
    if (viewName !== 'about') { // No specific JS for about page yet
        const script = document.createElement('script');
        script.id = 'view-script';
        script.src = `views/${viewName}/script.js`;
        script.defer = true; // Add defer attribute
        script.onload = setupCallback; // Call setupCallback after script loads
        document.body.appendChild(script);
    } else if (setupCallback) {
        setupCallback(); // For about page, call callback directly if no script
    }
}

function showCourses() {
    loadView('course-selection', () => {
        setupCoursesView(courses, showProblems);
    });
}

function showProblems(courseId) {
    loadView('problem-list', () => {
        setupProblemsView(courses, problems, courseId, showCourses, showProblem);
    });
}

function showProblem(problem, courseId) {
    loadView('problem-solving', () => {
        setupProblemSolvingView(problem, courseId, showProblems);
    });
}

function showAbout() {
    loadView('about');
}

showCourses();

homeButton.addEventListener('click', showCourses);

