let users = []

class Proceses {
    constructor() {
        this.nameProcess = ""
        this.comand = ""
        this.status = ""
    }
}



class User {
    constructor() {
        this.name = ""
        this.alias = ""
        this.processes = new Array()
    }

    addProcess(process) {
        this.processes.push(process)
    }
}


Statuses = {
    starting : "STARTING",
    stoping : "STOPING",
    working : "WORGING",
    stoped : "STOPED",
}


// Принимает proceses.json
// Преобразутет данные в обьет типа User
// Возвращает массив обьект типа User
function handleJson(data){
    let users = []

    data.forEach(el => {

        let userData = el  
        let user     = new User()

        user.name     = userData["name"]
        user.password = userData["password"]

        prcs = userData["processes"]

        prcs.forEach(prc => {
            let process = new Proceses()

            process.nameProcess = prc['nameProcess']
            process.comand      = prc['comand']
            process.status      = prc['status']

            user.addProcess(process)
        });
        users.push(user)
    });
    return users
}


function getProcessesData() {
    let objcts

    $.ajax({
        url: "scriptsPHP/getJsonFile.php",
        type: "post",
    datatype: 'json',
        async: false,
        success: function(data){
            // console.log(data)
            let json = $.parseJSON(data);
            objcts = handleJson(json["users"])
        },
        error: function(){

        }   
    });

    return objcts
}


function startProcess(user, process, statusField) {
    $.ajax({
        url: "scriptsPHP/sendStart.php",
        type: "post",
    datatype: 'json',
        data: {
            "action"     : "start",
            "userName"   : user.name, 
            "nameProcess": process.nameProcess, 
            "comand"     : process.comand
            },
        beforeSend: function() {
            // Set new status
            elem = $(`#${user.name}-${process.nameProcess}`).css({"background-color":"rgba(255, 208, 0, 0.555)"}).text("STARTING")
            console.log(elem)
        },
        success: function(data){
            console.log(data)
        },
        error: function(){
            alert("Не удалось запустить")
        }   
    });
}


function stopProcess(user, process) {
    $.ajax({
        url: "scriptsPHP/sendStart.php",
        type: "post",
    datatype: 'json',
        data: {
            "action"     : "stop",
            "userName"   : user.name, 
            "nameProcess": process.nameProcess, 
            // "comand"     : process.comand
            },
        beforeSend: function() {
            elem = $(`#${user.name}-${process.nameProcess}`).css({"background-color":"rgba(255, 208, 0, 0.555)"}).text("STOPPING")
        },
        success: function(data){
            console.log(data)
        },
        error: function(){
            alert("Не удалось запустить")
        }   
    });

}

// Устарело
function patternProcess(user, process){

    $('.'+user.name).append(

        $('<tr/>', {

            append: $('')
                .add($('<td/>', {
                    text:process.nameProcess
                }))
                .add($('<td/>', {
                    text:process.comand
                }))
                .add($('<td/>', {
                    text:process.status,
                    // id
                    id:`${user.name}-${process.nameProcess}`
                }))
                .add($('<td/>', {
                    append: $('')
                        .add($('<button/>', {
                            text:"Запустить",
                            on: {
                                click: function (event) {
                                    // console.log(this)
                                    startProcess(user, process)
                                }
                            }
                        }))
                        .add($('<button/>', {
                            text:"Остановить",
                            on: {
                                click: function (event) {
                                    stopProcess(user, process)
                                }
                            }
                        }))
                        .add($('<button/>', {
                            text:"Логи",
                            on: {
                                click: function (event) {
                                    // sendStartProcess()
                                }
                            }
                        }))
                }))
        })
    )
}

// Устарело
function patternUser(user) {
    $("<table/>", {

        class: "table",
        append: $('')

            .add($('<thead/>',{

                append: $('')
                    .add($('<th/>', {
                        text:user.name + " [Процесы]"
                    }))
                    .add($('<th/>', {
                        text:"Команда"
                    }))
                    .add($('<th/>', {
                        text:"Статус"
                    }))
                    .add($('<th/>', {
                        text:"Кнопки"
                    }))
            }))
            .add($('<tbody/>', {
                class: user.name
            }))

    }).appendTo('#body');
}


function processPattern(user, process) {

    $("<div/>", {
        class: "process d-flex flex-row justify-content-center w-100",
        
        append: $('')

            .add($('<div/>', {
                class: "nameProcess",
                text: process.nameProcess
            }))

            // Start button
            .add($('<button/>', {
                type: "button",
                class: "start proc-btns proc-btns-icons ml-left-5 stl-btns btn buttons ml-auto",
                on: {
                    click: function (event) {
                        startProcess(user, process)
                    }
                },
                append: $('')
                    .add($('<img/>', {
                        // src: "icons/play.svg",
                        src: "icons/play-button (1).svg",
                        alt: "Запусить"
                    }))
            }))

            // Stop button
            .add($('<button/>', {
                type: "button",
                class: "stop proc-btns proc-btns-icons ml-left-5 stl-btns btn buttons",
                on: {
                    click: function (event) {
                        stopProcess(user, process)
                    }
                },
                append: $('')
                    .add($('<img/>', {
                        src: "icons/primitive-square.svg",
                        alt: "Остановить"
                    }))
            }))

            // Status
            .add($('<div/>', {
                class: "status proc-btns d-flex justify-content-center stl-btns btn buttons",
                text: "Статус",
                style:"background-color: rgba(255, 208, 0, 0.555);",
                id:`${user.name}-${process.nameProcess}`
            }))

            // Href logs
            .add($('<a/>', {
                href:`logs.php?user=${user.name}&process=${process.nameProcess}`,
                target:"_blank",
                class:"btn btn-default buttons stl-btns proc-btns",
                text: "Logs"
            }))


    }).appendTo('#content');
}


function userPattern(user) {

    // console.log(user)
    if(isAdmin){
        $("<p/>", {
            class: "userName",
            text: user.alias
        }).appendTo('#content');
    }
}


function outAllInfo() {

    users.forEach(user => {
        let process  = user.processes

        // patternUser(user)
        userPattern(user)

        process.forEach(proc => {
            // patternProcess(user, proc)
            processPattern(user, proc)
        });
        
    });
}


// постоянное обновление статуса процесса из файла
const getStatuses = () => { 
        $.ajax({
            url: "scriptsPHP/getStatuses.php",
            type: "post",
        datatype: 'json',
            success: function(data){
                try
                {
                    let json = $.parseJSON(data);
                    processData(json)
                }
                catch (e)
                {
                    console.error("Can't load statuses.")
                    console.log(data)
                }
                
            },
            error: function(){
                console.log("Error")
            }   
        });

        setTimeout(() => {

            getStatuses()
        }, 1000 * 4);

        function processData(data) {
            
            users.forEach(user => {
                processes = user.processes
                userName = user.name

                processes.forEach(process => {
                    try{
                        u = data[userName]

                        if(u[process.nameProcess]){
                            
                            elem = $(`#${user.name}-${process.nameProcess}`).css({"background-color":"rgba(72, 192, 3, 0.459)"}).text("WORKING")
                        }
                        else {
                            elem = $(`#${user.name}-${process.nameProcess}`).css({"background-color":"rgba(192, 3, 3, 0.459)"}).text("STOPPED")
                        }
                    }catch (e){
                        elem = $(`#${user.name}-${process.nameProcess}`).css({"background-color":"rgba(192, 3, 3, 0.459)"}).text("STOPPED")
                    }
                });
            });
        }
}


function getinitData() {

    if (isAdmin) { return getAdminData() }
    else {         return getUserData() }

    function getUserData(){

        let users = []
    
        for (key in initDataJson) {
    
            let user = new User()
    
            let userData = initDataJson[key]
    
            user.name  = userData['name']
            user.alias = userData['alias']
    
            proc = userData['processes']
    
            for (pKey in proc) {
    
                let process = new Proceses()
    
                process.nameProcess = pKey
                process.comand      = proc[pKey]
                process.status      = ""
    
                user.addProcess(process)
            };  
    
            users.push(user)
         }
    
         return users
    }
    function getAdminData() {

        let users = []
    
        for (key in initDataJson) 
        {
            let user = new User()
    
            let userData = initDataJson[key]
    
            user.name  = key
            user.alias = userData['name']
    
            proc = userData['processes']
    
            for (pKey in proc) 
            {
                let process = new Proceses()
    
                process.nameProcess = pKey
                process.comand      = proc[pKey]
                process.status      = ""
    
                user.addProcess(process)
            }
    
            users.push(user)
        }
    
        return users
    }
}


function onLoad() 
{
    users = getinitData()

    outAllInfo()
    getStatuses()
}

onLoad()