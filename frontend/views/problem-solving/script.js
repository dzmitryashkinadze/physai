function setupProblemSolvingView(problem, courseId, showProblems) {
    

    const problemStatementContent = document.querySelector('#problem-statement .column-content');
    const equationsContainer = document.getElementById('equations-container');
    const submitButton = document.getElementById('submit-solution');
    problemStatementContent.innerHTML = `<h3>${problem.title}</h3><p>${problem.description}</p>`;

    const mathFields = []; // Array to store MathQuill instances

    const addEquationButton = document.getElementById('add-equation');

    function addEquationInput() {
        const newEquationDiv = document.createElement('div');
        newEquationDiv.className = 'equation-input-field';
        newEquationDiv.id = `equation-field-${mathFields.length}`; // Assign a unique ID
        newEquationDiv.name = `equation-field-${mathFields.length}`; // Assign a unique name for form field compliance
        newEquationDiv.style.width = '100%';
        newEquationDiv.style.border = '1px solid #ccc';
        newEquationDiv.style.padding = '10px';
        newEquationDiv.style.marginBottom = '10px'; // Add some spacing

        const mathFieldContainer = document.createElement('span');
        mathFieldContainer.className = 'math-field-container';
        newEquationDiv.appendChild(mathFieldContainer);

        const removeButton = document.createElement('button');
        removeButton.textContent = 'x';
        removeButton.className = 'remove-equation-button';
        newEquationDiv.appendChild(removeButton);

        equationsContainer.appendChild(newEquationDiv);

        const MQ = MathQuill.getInterface(2).MathField(mathFieldContainer, {
            spaceBehavesAsTab: true,
            handlers: {
                edit: function() {
                    // Removed automatic addition of new fields
                },
                enter: function(mathField) {
                    addEquationInput();
                }
            }
        });
        mathFields.push(MQ);
        
        removeButton.addEventListener('click', () => {
            removeEquationInput(newEquationDiv, MQ);
        });

        MQ.focus(); // Focus on the newly created field
    }

    function removeEquationInput(equationDiv, mathFieldInstance) {
        equationDiv.remove();
        const index = mathFields.indexOf(mathFieldInstance);
        if (index > -1) {
            mathFields.splice(index, 1);
        }
    }

    // The first equation input field will be added when the "Add Equation" button is clicked.

    addEquationButton.addEventListener('click', addEquationInput); // Add event listener for the button
    addEquationInput(); // Add one equation input field on page load

    // Toolbar functionality
    const dropdownButton = document.querySelector('.dropbtn');
    const dropdownContent = document.querySelector('.dropdown-content');

    dropdownButton.addEventListener('click', (event) => {
        dropdownContent.classList.toggle('show');
        event.stopPropagation(); // Prevent the click from propagating to the document
    });

    // Close the dropdown if the user clicks outside of it
    window.addEventListener('click', (event) => {
        if (!event.target.matches('.dropbtn')) {
            if (dropdownContent.classList.contains('show')) {
                dropdownContent.classList.remove('show');
            }
        }
    });

    const toolbarButtons = document.querySelectorAll('.toolbar-button');
    toolbarButtons.forEach(button => {
        button.addEventListener('click', () => {
            const latexCommand = button.dataset.latex;
            // Find the currently focused MathQuill field
            const activeMQ = mathFields.find(mq => mq.el() === document.activeElement || mq.el().contains(document.activeElement));
            if (activeMQ) {
                activeMQ.cmd(latexCommand).focus();
            } else if (mathFields.length > 0) {
                // If no field is focused, use the last one
                mathFields[mathFields.length - 1].cmd(latexCommand).focus();
            }
        });
    });

    submitButton.addEventListener('click', () => {
        const allSolutionsLatex = mathFields.map(mq => mq.latex()).filter(latex => latex.length > 0);
        console.log("Submitted LaTeX solutions:", allSolutionsLatex);
        // Here you would typically send allSolutionsLatex to your backend
    });

    renderMathInElement(problemStatementContent, {
      // customised options
      // • auto-render specific keys, e.g.:
      delimiters: [
        {left: '$$', right: '$$', display: true},
        {left: '$', right: '$', display: false},
        {left: '\(', right: '\)', display: false},
        {left: '[\]', right: '[]', display: true}
      ],
      // • rendering keys, e.g.:
      throwOnError: false
    });
}