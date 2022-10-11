const header = document.querySelector('#header');
const sidebox = document.querySelector('.side_box');
const variableWidth = document.querySelectorAll('.contents_box .contents');
const delegation = document.querySelector('.contents_box');


function delegationFunc(e) {

    let elem = e.target;

    console.log(elem);

    while (!elem.getAttribute('data-name')) {
        elem = elem.parentNode;

        if (elem.nodeName === 'BODY') {
            elem = null;
            return;
        }
    } 
    elem.classList.toggle('on');

}


function resizeFunc() {

    if (pageYOffset >= 10) {

        let calcWidth = (window.innerWidth * 0.5) + 167;

        sidebox.style.left = calcWidth + 'px';
    }


    if (matchMedia('screen and (max-width : 800px)').matches) {

        for (let i = 0; i < variableWidth.length; i++) {
            variableWidth[i].style.width = window.innerWidth - 20 + 'px';
        }

    } else {

        for (let i = 0; i < variableWidth.length; i++) {

            if (window.innerWidth > 600) {
                variableWidth[i].removeAttribute('style');
            }

        }

    }

}

function scrollFunc() {

    var scrollHeight = pageYOffset + window.innerHeight;
    var documentHeight = document.body.scrollHeight;



    if (pageYOffset >= 10) {
        header.classList.add('on');


        if (sidebox) {
            sidebox.classList.add('on');
        }

        resizeFunc();


    } else {
        header.classList.remove('on');

        if (sidebox) {
            sidebox.classList.remove('on');
            sidebox.removeAttribute('style');
        }

    }

    console.log('scrollHeight : '+scrollHeight);
    console.log('documentHeight : ' +documentHeight);

    if (scrollHeight >= documentHeight) {

        var page = document.querySelector('#page').value;

        document.querySelector('#page').value = parseInt(page) + 1;

        callMorePostAjax(page);

        if(page > 10){
            return;
        }

    }

}

function callMorePostAjax(page) {

    if(page > 10){
        return;
    }

    $.ajax({
        type: 'POST',
        url: "./post.html",
        data: {
            'page': page,
        },
        success: addMorePostAjax,
        dataType: 'html',
    });

}

function addMorePostAjax(data, textStatus, jqXHR) {

    delegation.insertAdjacentHTML("beforeend", data);
}

setTimeout(function () {
    scrollTo(0, 0)
}, 100);


if (delegation) {
    delegation.addEventListener('click', delegationFunc);
}


window.addEventListener('resize', resizeFunc);
window.addEventListener('scroll', scrollFunc);