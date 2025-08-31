function setupCoursesView(courses, showProblems) {
    const courseList = document.getElementById('course-list');
    courseList.innerHTML = '';
    courses.forEach(course => {
        const li = document.createElement('li');
        li.textContent = course.title;
        li.addEventListener('click', () => showProblems(course.id));
        courseList.appendChild(li);
    });
}