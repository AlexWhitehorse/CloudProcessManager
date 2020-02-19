
function GET(name){
    if(name=(new RegExp('[?&]'+encodeURIComponent(name)+'=([^&]*)')).exec(location.search))
       return decodeURIComponent(name[1]);
}

const NAME_USER = GET('user');
const NAME_PROCESS = GET('process');
let flagUpdate = true;
let autoScrolling = true;
let feqUpdate = 4000; //ms




function getLog(user, process) {
        $.ajax({
            url: "scriptsPHP/GetLogs.php",
            get: "post",
            data: {'user' : user, "process": process},
        datatype: 'json',
            success: function(data){
                console.log(data)
                let text = ''

                let json = $.parseJSON(data);

                if(json) 
                {
                    json.map(function(elem) 
                    {
                        text += elem + ' <br>';
                    });

                    // ($('#outText').text(text))
                    $('#outText').append(
                                        `<div id="outText">
                                            ${text}
                                        </div>`
                                        );
                }
                else $('#outText').text('Нет логов');

                if(autoScrolling)
                {
                    
                    $([document.documentElement, document.body]).animate({
                       
                        scrollTop: $('#outText').prop('scrollHeight')
                    }, 0);
                }
                
            },
            error:function(){
            }   
        });
    
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


const regularUpdates = () => {

    if(flagUpdate)
    {
        getLog(NAME_USER, NAME_PROCESS);
    }
    
    setTimeout(() => {

        regularUpdates()
    }, feqUpdate);
}



regularUpdates();

// ========== Buttons ===========
$(document).on('click',"#scrolling", function(){
    autoScrolling = changeFlag(autoScrolling, '#scrolling');
});

$(document).on('click',"#update-logs", function(){
    flagUpdate = changeFlag(flagUpdate, '#update-logs');
});
