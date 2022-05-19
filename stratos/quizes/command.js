//Invoker
class Invoker {
    action(type) {
        var receiver = new action();
        receiver.action(type);
    }
}

//Concrete Command
class QuizCommand {
    SetCommand(command) {
        this.command = command;
    }

    execute(data) {
        const amount = document.getElementById('num_of_question')
        const difficulty = document.querySelector('#difficult')
        const choice = document.querySelector('#cho')
        const data = {}
        const csrf = document.getElementsByName('csrfmiddlewaretoken')
        data['csrfmiddlewaretoken'] = csrf[0].value
        data['amount'] = amount.value
        data['difficulty'] = difficulty.value
        data['choice'] = choice.value
        data['type'] = "multiple"

        $.ajax({
            type: 'POST',
            url: `${url}`,
            data: data,
            success: function (response) {
                addForm.classList.add('not-visible')
                quiForm.classList.remove('not-visible')
                modalBtn.classList.remove('not-visible')
                saveBtn.classList.remove('not-visible')
                goibibo.forEach(goib => {
                    goib.classList.remove('not-visible')

                })

                const data = response.data
                maindata = data
                showData(data)

            },

            error: function (response) {
                console.log(response)
            }
        })
    }

    undo() {
        document.getElementById('#undoBtn').onclick = function () {
            window.location.reload();
        };
    }
}

//Concrete Command
class QuizCommand {
    SetCommand(command) {
        this.command = command
    }

    execute(data) {
        const elements = [...document.getElementsByClassName('ans')]
        data['csrfmiddlewaretoken'] = csrf[0].value
        elements.forEach(el => {
            if (el.checked) {
                data[el.name] = el.value
            } else {
                if (!data[el.name]) {
                    data[el.name] = null
                }
            }
        })

        $.ajax({
            type: 'POST',
            url: `${url}save`,
            data: data,
            success: function (response) {

                const result = response.results
                console.log(response.passed)
                quizForm.classList.add('not-visible')

                scoreBox.innerHTML += `<b>${response.passed ? 'Congratulations!!':'opps'} Your result is ${response.score}%</b> `

                result.forEach(res => {
                    const resDiv = document.createElement('div')
                    for (const [question, resp] of Object.entries(res)) {
                        resDiv.innerHTML += question

                        const cls = ['container', 'p-3', 'text-light', 'h6']
                        resDiv.classList.add(...cls)

                        if (resp == 'not answered') {
                            resDiv.innerHTML += '- not answered'
                            resDiv.classList.add('bg-danger')
                        } else {
                            const answer = resp['answered']
                            const correct = resp['correct_answer']

                            if (answer == correct) {
                                resDiv.classList.add('bg-success')
                                resDiv.innerHTML += `answered:${answer}`
                            } else {
                                resDiv.classList.add('bg-danger')
                                resDiv.innerHTML += `correct answered:${correct}`
                                resDiv.innerHTML += `answered ${answer}`
                            }
                        }

                    }
                    resultBox.append(resDiv)
                })
            },
            error: function (response) {
                console.log(response)
            }
        })
    }

    undo() {
        document.getElementById('#undoBtn').onclick = function () {
            window.location.reload();
        };
    }
}

//   Receiver
class Receiver {
    action(type) {
        if (type === "question") {
            var quiz = new AddQuiz();
            quiz.addQuiz();
        } else if (type === "result") {
            var quizResults = new AddResult();
            quizResults.addResult();
        }
    }
}