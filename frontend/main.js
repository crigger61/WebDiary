var API_BASE_URL;

async function api_get(path = '', data = ''){
    let resp = await fetch(API_BASE_URL+path+'?'+new URLSearchParams(data), {
        method: 'GET',
        headers: {
                'Accept': 'application/json',
                'X-API-Key': localStorage.X_API_KEY
            }
        }
    )
    return await resp.json()
}
async function api_post(path = '', data = ''){
    let resp = await fetch(API_BASE_URL+path, {
        method: 'POST',
        body: data,
        headers: {
                'Accept': 'application/json',
                'X-API-Key': localStorage.X_API_KEY
            }
        }
    )
    return await resp.json()
}
async function api_put(path = '', data = ''){
    let resp = await fetch(API_BASE_URL+path, {
        method: 'PUT',
        body: data,
        headers: {
                'Accept': 'application/json',
                'X-API-Key': localStorage.X_API_KEY
            }
        }
    )
    return await resp.json()
}async function api_patch(path = '', data = ''){
    let resp = await fetch(API_BASE_URL+path, {
        method: 'PATCH',
        body: data,
        headers: {
                'Accept': 'application/json',
                'X-API-Key': localStorage.X_API_KEY
            }
        }
    )
    return await resp.json()
}async function api_delete(path = '', data = ''){
    let resp = await fetch(API_BASE_URL+path, {
        method: 'DELETE',
        body: data,
        headers: {
                'Accept': 'application/json',
                'X-API-Key': localStorage.X_API_KEY
            }
        }
    )
    return await resp.json()
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