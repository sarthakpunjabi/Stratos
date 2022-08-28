console.log("hello world")

const modalBtns = [...document.getElementsByClassName('modal-button')]
console.log(modalBtns)
const modalBody = document.getElementById('modal-body-confirm')
const removeBtn = [...document.getElementsByClassName('remove-button')]
const startBtn = document.getElementById('start-button')
const url = window.location.href




modalBtns.forEach(modalBtn => modalBtn.addEventListener('click',()=>{
    const pk = modalBtn.getAttribute('data-pk')
    const name = modalBtn.getAttribute('data-quiz')
    const numQuestion = modalBtn.getAttribute('data-questions')
    const difficulty = modalBtn.getAttribute('data-difficulty')
    const scoreToPass = modalBtn.getAttribute('data-pass')
    const time = modalBtn.getAttribute('data-time')

    modalBody.innerHTML = `
        <div class="h5 mb-3">Are You Sure you want to begin" <b>${name}</b>"?</div>
        <div class="text-muted">
            <ul>
                <li>difficulty: <b>${difficulty}</b> </li>
                <li>number of questions: <b>${numQuestion}</b> </li>
                <li>score to pass: <b>${scoreToPass}%</b> </li>
                <li>time: <b>${time} min</b> </li>
            </ul>
        </div>
    `
    startBtn.addEventListener('click',()=>{
        window.location.href = url + pk
    })
}))

function getCookie(name) {
    var dc = document.cookie;
    var prefix = name + "=";
    var begin = dc.indexOf("; " + prefix);
    if (begin == -1) {
        begin = dc.indexOf(prefix);
        if (begin != 0) return null;
    }
    else
    {
        begin += 2;
        var end = document.cookie.indexOf(";", begin);
        if (end == -1) {
        end = dc.length;
        }
    }
    // because unescape has been deprecated, replaced with decodeURI
    //return unescape(dc.substring(begin + prefix.length, end));
    return decodeURI(dc.substring(begin + prefix.length, end));
}

removeBtn.forEach(rbtn => rbtn.addEventListener('click',()=>{
    console.log("Remove")
    const data = {}
    data['pk'] = rbtn.getAttribute('data-pk')
    data['name'] = rbtn.getAttribute('data-quiz')
    data['csrfmiddlewaretoken'] = getCookie("csrftoken")
    console.log('achieved',data)
    $.ajax({
        type:'POST',
        url:`${url}remove`,
        data:data,
        success:function(response){
                window.location.replace(url);
                console.log(response)
        },
        error:function(response){
                console.log(response)

        }
    })


}))