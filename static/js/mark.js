// 定义 log
const log = console.log.bind(console)

const e = function(selector) {
  return document.querySelector(selector)
}


const es = function(selector) {
  return document.querySelectorAll(selector)
}


const bindEvent = function(element, eventName, callback) {
  element.addEventListener(eventName, callback)
}


const bindAll = function(selector, eventName, callback) {
    var elements = es(selector)
    for (var i = 0; i < elements.length; i++) {
    var element = elements[i]
    bindEvent(element, eventName, callback)
  }
}


var find = function(element, selector) {
    return element.querySelector(selector)
}


var appendHtml = function(element, html) {
  element.insertAdjacentHTML( 'beforeend', html)
}


var toggleClass = function(element, className) {
    if (element.classList.contains(className)) {
        element.classList.remove(className)
    } else {
        element.classList.add(className)
    }
}


const ajax = function(method, path, data, responseCallback) {
    log('ajax request', method, path, data, responseCallback)
    var r = new XMLHttpRequest()
    r.open(method, path, true)
    r.setRequestHeader('Content-Type', 'application/json')
    r.onreadystatechange = function() {
        if(r.readyState === 4) {
            responseCallback(r)
        }
    }
    data = JSON.stringify(data)
    r.send(data)
}
