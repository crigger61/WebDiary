var API_BASE_URL;

async function api_get(path = '', data = ''){
    let resp = await fetch(API_BASE_URL+path+'?'+new URLSearchParams(data), {
        method: 'GET',
        headers: {
                'Accept': 'application/json',
                'X-API-Key': getJWT()
            }
        }
    )
    let resp_json = await resp.json()
    updateJWT(resp_json)
    return resp_json
}
async function api_post(path = '', data = ''){
    let resp = await fetch(API_BASE_URL+path, {
        method: 'POST',
        body: JSON.stringify(data),
        headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'X-API-Key': getJWT()
            }
        }
    )
    let resp_json = await resp.json()
    updateJWT(resp_json)
    return resp_json
}
async function api_put(path = '', data = ''){
    let resp = await fetch(API_BASE_URL+path, {
        method: 'PUT',
        body: JSON.stringify(data),
        headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'X-API-Key': getJWT()
            }
        }
    )
    let resp_json = await resp.json()
    updateJWT(resp_json)
    return resp_json
}async function api_patch(path = '', data = ''){
    let resp = await fetch(API_BASE_URL+path, {
        method: 'PATCH',
        body: JSON.stringify(data),
        headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'X-API-Key': getJWT()
            }
        }
    )
    let resp_json = await resp.json()
    updateJWT(resp_json)
    return resp_json
}async function api_delete(path = '', data = ''){
    let resp = await fetch(API_BASE_URL+path, {
        method: 'DELETE',
        body: JSON.stringify(data),
        headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'X-API-Key': getJWT()
            }
        }
    )
    let resp_json = await resp.json()
    updateJWT(resp_json)
    return resp_json
}

function getJWT(){
    return localStorage.X_API_KEY;
}

function updateJWT(resp){
    if(resp.new_token !== null) {
        localStorage.X_API_KEY = resp.new_token;
        console.log('Updated JWT')
    }
}




function add_component(comp_id, speed=200){
    $('#cover').show()
    $('[comp_id='+comp_id+']').show()
    $('#cover').fadeOut(speed)
}
function del_component(comp_id, speed=200){
    $('#cover').show()
    $('[comp_id='+comp_id+']').show()
    $('#cover').fadeOut(speed)
}
function show_component(comp_id, speed=200){
    $('#cover').show()
    $('[comp_id]').hide()
    $('[comp_id='+comp_id+']').show()
    $('#cover').fadeOut(speed)
}
function flash_cover(speed=200){
    $('#cover').show()
    $('#cover').fadeOut(speed)
}





function open_main_page(){

}
function open_login_page(){

}





async function main(){
    while(true){
        try {
            let resp = await (await fetch(localStorage.API_BASE_URL)).json()
            if (resp.status == 200 && resp.data.Application_Name == 'WebDiary')
                break
        }catch {}
        localStorage.API_BASE_URL = prompt('Please enter the api url.')
    }
    if(!localStorage.API_BASE_URL.endsWith('/'))
        localStorage.API_BASE_URL += '/'
    API_BASE_URL = localStorage.API_BASE_URL;
}






$(document).ready(main)