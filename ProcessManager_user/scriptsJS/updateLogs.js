function GET(name){
    if(name=(new RegExp('[?&]'+encodeURIComponent(name)+'=([^&]*)')).exec(location.search))
       return decodeURIComponent(name[1]);
}

const NAME_USER = GET('user');
const NAME_PROCESS = GET('process');
let flagUpdate = true;
let autoScrolling = true;
let TimeLastLog = Date.now();
let feqUpdate = 500; //ms

let msgPattern = {
    procId: `${NAME_USER}/${NAME_PROCESS}`,
    tsFrom: TimeLastLog
}

const changeFlag = (flag, classChange) => {
    if(flag == true)
    {
        flag = false;
        $(classChange).addClass('white-color');
    }
    else if (flag == false) 
    {
        flag = true;
        $(classChange).removeClass('white-color');
    }
    return flag;
}


// ======DEBUG======
function askLog(user, process) {

    let msg = JSON.stringify({}) 
    // console.log('here')
    $.ajax({
        url: "scriptsPHP/redirectLogMsg.php",
        get: "get",
        // data: {'user' : user, "process": process},
        data: {"message": msgPattern},
     timeout: 300,
    datatype: 'json',
        success: function(data){
            console.log("Data: " + data)

            let lastIndex = data.lastIndexOf('}') + 1
            let substr = data.substring(0, lastIndex) + ']'

            console.log("Data: " + substr)

            // console.log(msgPattern)
            let message = {}
            try {   
                message = JSON.parse(substr)
            } catch (SyntaxError) {
                // console.log(SyntaxError)
                return
            }   
            

            // Out to page
            let arrMsg = message.pop();
            // arrMsg = message.pop();
            let toPage = message.filter(el => el.ts >= msgPattern.tsFrom)
            msgPattern.tsFrom = arrMsg.ts

            function gesStrOut(obj) {
                let str = '';
                obj.map(el => str += (el.txt + '<br/>'))
                return str
            }

            console.log("Date now: " + msgPattern.tsFrom)

            $('#outText').append(function () {
                return (`<div id="outText">
                          ${gesStrOut(toPage)}
                         </div>`)
            })
            // toPage.map(el => console.log(el.txt))
            // console.log("Sended: " + toString({"message": msgPattern}))
            // console.log("Reseived: " + data)
            // console.log(toPage)

            if(autoScrolling) {
                
                $([document.documentElement, document.body]).animate({
                    
                    scrollTop: $('#outText').prop('scrollHeight')
                }, 0);
            }
        },
        error:function(data){
            console.log(data)
        }   
    });
}
const OutNewLineLog = () => {
    if(flagUpdate)
    {   
        askLog(NAME_USER, NAME_PROCESS);
    }
    setTimeout(() => {

        OutNewLineLog();
    }, feqUpdate);
}

OutNewLineLog();
// ========== Buttons ===========
$(document).on('click',"#scrolling", function(){
    autoScrolling = changeFlag(autoScrolling, '#scrolling');
});

$(document).on('click',"#update-logs", function(){
    flagUpdate = changeFlag(flagUpdate, '#update-logs');
});
