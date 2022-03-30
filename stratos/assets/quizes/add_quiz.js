console.log("Add_quiz")

const addForm = document.getElementById('addForm')
const submit = document.querySelector('#submit')
const modalBtn = document.getElementById('modbtn')
const url = window.location.href
const saveBtn = document.getElementById('savebtn')
const quizBox = document.getElementById('quiz-box')
const quiForm = document.getElementById('quiz-form')
const saveModalBtn = document.getElementById('save-modal-form')
const modalForm = document.getElementById('modal-form')
const question = document.getElementById('addquestion')
const incorrect = [...document.getElementsByClassName('op')]
const correct = document.getElementById('op4')
const goibibo = [...document.getElementsByClassName('goibibo')]
let maindata

const showData = (data) => {
    quizBox.innerHTML = ""
    quizBox.innerHTML += `
        <div class="mb-2">
            <b><h1>${data[1].category}</h1></b>
        </div>
        `
    console.log(data)
    data.forEach(el => {
        quizBox.innerHTML += `
                    <hr>
                    <div class="mb-2">
                        <b>${el.question}</b>
                    </div>
                    
                `
        el.incorrect_answers.forEach(answer => {
            quizBox.innerHTML += `
                        <div>
                            <input type='radio' class='ans' id='${el.question}-${answer}' name='${el.question}' value='${answer}' disabled>
                            <label for='${el.question}'>${answer}</label>
                        </div>
                        
                    `
        })

        quizBox.innerHTML += `
                <div>
                    <input type='radio' class='ans' id='${el.question}-${el.correct_answer}' name='${el.question}' value='${el.correct_answer}' checked>
                    <label for='${el.question}'>${el.correct_answer}</label>
                </div>
                <br>
                `

    })
}

const sendData = () => {
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

addForm.addEventListener('submit', e => {
    e.preventDefault()
    sendData()

})

saveModalBtn.addEventListener('click', e => {
    e.preventDefault()
    incans = []
    incorrect.forEach(inc => {
        incans.push(inc.value)
        inc.value = ""
    })
    obj = {
        "question": question.value,
        "correct_answer": correct.value,
        "incorrect_answers": incans
    }
    incans = []
    question.value = ""
    correct.value = ""
    maindata.push(obj)
    showData(maindata)

})

saveBtn.addEventListener('click', e => {
    e.preventDefault()
    const goinp = [...document.getElementsByClassName('goinp')]
    const csrftoken = document.getElementsByName('csrfmiddlewaretoken')[0].value
    metaData = {}
    goinp.forEach(going => {
        metaData[going.getAttribute('name')] = going.value
    })
    $.ajax({
        type: 'POST',
        url: `${url}save`,
        headers: {
            "X-CSRFToken": csrftoken
        },
        data: {
            "data": maindata,
            "meta": metaData
        },
        success: function (response) {
            console.log(response)
            window.location = "/"
        },
        error: function (response) {
            console.log(response)
        }
    })
})

//Invoker
class Quiz {
    save(type) {
        var receiver = new Save();
        receiver.execute(type);
    }

    undo(type) {
        var receiver = new Save();
        receiver.undo();
    }
}

//Concrete Command
class AddQuiz {
    constructor(valueToAdd) {
        this.valueToAdd = valueToAdd
    }

    addQuiz(data) {
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
class AddResult {
    constructor(data) {
        this.data = data
    }

    addResult(data) {
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
class Save {

    execute(type) {
        if (type === "question") {
            var quiz = new AddQuiz();
            quiz.addQuiz();
        } else if (type === "result") {
            var quizResults = new AddResult();
            quizResults.addResult();
        }
    }

    undo() {
        document.getElementById('#undoBtn').onclick = function () {
            window.location.reload();
        };
    }
}