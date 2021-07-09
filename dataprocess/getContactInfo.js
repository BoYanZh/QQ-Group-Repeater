//Used in exployer
//Modified from https://github.com/BoYanZh/QQ-Group-Repeater/issues/13
(function() {
    const profs = document.getElementsByClassName("information");
    const pics = document.getElementsByClassName("person_img");
    let data = [];
    for (let i=0;i<profs.length;i++) {
      const titles = profs[i].getElementsByClassName("title");
      const pic=pics[i].childNodes[0];
      data.push({
        "name": titles[0].innerText,
        "title": titles[1].innerText,
        "office": titles[2].nextElementSibling.innerText,
        "tel": titles[3].nextElementSibling.innerText,
        "email": titles[4].nextElementSibling.innerText,
        "imageUrl": pic.firstChild.currentSrc,
        "selfIntrUrl": pic.href,
      })
    }
    return data;
  })()