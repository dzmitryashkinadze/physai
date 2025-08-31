function setupProblemsView(courses, problems, courseId, showCourses, showProblem) {
    const course = courses.find(c => c.id === courseId);
    const courseTitle = document.getElementById('course-title');
    const problemList = document.getElementById('problem-list');
    

    courseTitle.textContent = course.title;
    problemList.innerHTML = '';
    problems[courseId].forEach(problem => {
        const li = document.createElement('li');
        li.textContent = problem.title;
        li.addEventListener('click', () => showProblem(problem, courseId));
        problemList.appendChild(li);
    });
    
}