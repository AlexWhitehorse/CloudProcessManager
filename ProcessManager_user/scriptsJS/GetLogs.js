
function GET(name){
    if(name=(new RegExp('[?&]'+encodeURIComponent(name)+'=([^&]*)')).exec(location.search))
       return decodeURIComponent(name[1]);
}

const NAME_USER = GET('user');
const NAME_PROCESS = GET('process');
let flagUpdate = true;
let autoScrolling = true;
let feqUpdate = 500; //ms
// let logsUpdate = 60100;

// function sendMakeLog(user, process) {
//     $.ajax({
//         url: "scriptsPHP/logProc.php",
//         get: "get",
//         data: {'user' : user, "process": process},
//     datatype: 'json',
//         success: function(data){
//         },
//         error:function(){}   
//     });
// }
/*
function getLog(user, process) {
        $.ajax({
            url: "scriptsPHP/GetLogs.php",
            get: "post",f(autoScrolling) {
                
                $([document.documentElement, document.body]).animate({
                    
                    scrollTop: $('#outText').prop('scrollHeight')
                }, 0);
            }
            data: {'user' : user, "process": process},
        datatype: 'json',
            success: function(data){
                
                let text = ''
                let json = $.parseJSON(data);
                

                if(json != 'false') {
                    json.splice(0, 1)
                    json.map(function(elem) {
                        text += elem + ' <br>';
                    });

                    // ($('#outText').text(text))
                    $('#outText').append(
                                        `<div id="outText">
                                            ${text}
                                        </div>`
                                        );
                }
                else $('#mainPage').text('Нет логов');

                if(autoScrolling) {
                    
                    $([document.documentElement, document.body]).animate({
                       
                        scrollTop: $('#outText').prop('scrollHeight')
                    }, 0);
                }
                
            },
            error:function(){
            }   
        });
    
}
*/

function getLog(user, process) {


    let file = `${user}_${process}.txt`;

    try {
        $.ajax({
            url: `logs/${file}`,
            get: "get",
            success: function(data){
                // если файл сусществует
    
                // $('#outText').append(
                //     `<div id="outText">
                //         ${data}
                //     </div>`
                //     );
                $('#outText').replaceWith(function () {
                    return (`<div id="outText">
                              ${data}
                             </div>`)
                })
    
                if(autoScrolling) {
                    
                    $([document.documentElement, document.body]).animate({
                        
                        scrollTop: $('#outText').prop('scrollHeight')
                    }, 0);
                }
    
            },
            error:function(){
                console.log('error')
                getLog(user, process)
            }   
        });
    } catch (error) {
        console.log(error)
        getLog(user, process)
    }
    

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


// const regularUpdates = () => {

//     if(flagUpdate)
//     {
//         getLog(NAME_USER, NAME_PROCESS);
//     }
    
//     setTimeout(() => {

//         regularUpdates()
//     }, feqUpdate);
//     // getLog(NAME_USER, NAME_PROCESS)
// }

// const updateLogs = () => {
//     if(flagUpdate)
//     {   
//         sendMakeLog(NAME_USER, NAME_PROCESS);
//     }
    
//     setTimeout(() => {

//         updateLogs()
//     }, logsUpdate);
// }


// updateLogs();
// regularUpdates();

// ======DEBUG======
function askLog(user, process) {
    // console.log('here')
    $.ajax({
        url: "scriptsPHP/getOneLineLog.php",
        get: "get",
        data: {'user' : user, "process": process},
    datatype: 'json',
        success: function(data){

            $('#outText').append(function () {
                return (`<div id="outText">
                          ${data}
                         </div>`)
            })

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
