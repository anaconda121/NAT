// COLLAPSIBLE VIEW FUNCTION
var coll = document.getElementsByClassName("collapsible");
var i;

for (i = 0; i < coll.length; i++) {
  coll[i].addEventListener("click", function() {
    this.classList.toggle("active");
    var content = this.nextElementSibling;
    if (content.style.maxHeight){
      content.style.maxHeight = null;
    } else {
      content.style.maxHeight = content.scrollHeight + "px";
    } 
  });
}


// FADE OUT ALERTS
var close = document.getElementsByClassName("btn-close");
var i;

for (i = 0; i < close.length; i++) {
  close[i].onclick = function(){
    var div = this.parentElement;
    div.style.opacity = "0";
    setTimeout(function(){ div.style.display = "none"; }, 600);
  }
}


// TABLESORTER
$(function() {
  $("table").tablesorter();
});


// CONDITIONAL FORM FOR PATIENT ANNOTATION
$('#id_SyndromicDiagnosis, id_LabelCertainty').show();
var selected = $('#id_SyndromicDiagnosis option:selected').text();
if (selected == 'Mild Cognitive Impairment' || selected == 'Dementia') {
  $('.id_DementiaSeverity').show();
} else {
  $('.id_DementiaSeverity').hide();
}

$('#id_SyndromicDiagnosis').change(function () {
  selected = $('#id_SyndromicDiagnosis option:selected').text();
  if (selected == 'Mild Cognitive Impairment' || selected == 'Dementia') {
    $('.id_DementiaSeverity').show();
  } else {
    $('.id_DementiaSeverity').hide();
  }
});


// TABULATION FOR TIMELINE
/*
function onTabClick(event) {
  let activeTabs = document.querySelectorAll('.active');

  // deactivate existing active tab and panel
  for(let i = 0; i < activeTabs.length; i++) {
    console.log(activeTabs[i].className);
    activeTabs[i].className = activeTabs[i].className.replace('active', '');
  }

  // activate new tab and panel
  let passiveType = "#" + event.target.href.split('#')[1];
  let passiveTabs = document.querySelectorAll(passiveType);

  for(let i = 0; i < passiveTabs.length; i++) {
    passiveTabs[i].className += ' active';
  }
}

const element = document.getElementById('nav-tab');
element.addEventListener('click', onTabClick);*/

// SCROLLING TO CURRENT NOTE ON TIMELINE

$(document).ready(function(){
  var url = window.location.href;

  var splitBySlash = url.split("/");
  console.log(splitBySlash);
  
  var finalId = splitBySlash[4] + "-" + splitBySlash[5] + "-timeline";
  console.log(finalId);

  jQuery(".timeline").animate({  
    scrollTop: jQuery("#" + finalId).offset().top
  });

  var counter = 0;
  var keywords = document.getElementsByClassName('keyword');  
  var dist = 0;
  console.log(keywords);
  var txt = document.getElementsByClassName('keyword-text')[0].textContent;
  console.log("txt + ", txt);
  var txtArr = txt.split(" ");
  var wordCount = txtArr[2];
  console.log("wordCount + " , wordCount);

  $("#first-keyword-button").click(function(){
    console.log("counter: " + counter);
    console.log(keywords);
    
    for (var x = 0; x < keywords.length; x++) {
      keywords[x].id = 'keyword-inactive';
    }

    

    //console.log("keywords: ", keywords, " len, ", keywords.length);
    //console.log("keywords inx: " + keywords[counter]);
    keywords[counter].id = 'keyword-active';
    
    //console.log("keywords counter: ", keywords[counter], " ", keywords[counter].id, " len, ", keywords.length);
    //console.log("keywords counter-1: ", keywords[counter-1], " ", keywords[counter-1].id, " len, ", keywords.length);

    //var elem = document.getElementById("keywords-active");
    //elem.scrollIntoView();
    //document.getElementById("keywords-active").scrollTop(dist)
    dist += $("#keyword-active").offset().top-350;
    console.log("px that is needed to scroll: " + dist);

    jQuery("#note-text").animate({  
      scrollTop: dist
    });
    
    //var ele = $("#keyword-active");
    //$("#note-text").scrollTop($("#keyword-active").offset().top - $(window).scrollTop());
    //$("#note-text").scrollTo("#keyword-active");


    counter++;
    counter = counter % keywords.length;

  });
});


// SCROLL TO FIRST KEYWORD IN NOTE
