
//Select the HTML form and results section
let resultsTag = document.getElementsByClassName("results")[0]
let form = document.getElementById('form');

//get all Timelineposts from the Database
fetch('/api/timeline_post')
.then(res =>{
    if(res.ok) {console.log("GET request successful")}
    else {console.log("GET request unsuccessful")}
    return res
})
.then(res => res.json())
.then(data => loadTimelinePosts(data.timeline_posts));

/*This function displays all the timeline posts in the database on the page, given an array of timeline posts*/
loadTimelinePosts = arr => {
    resultsTag.innerHTML = "";  //clear the results section

    //GET fetch brings the Timeline objects from the database in descending order, thus
    //iterate the array backwards (ascending) b/c showPost() will display in descending order i.e. the most recent post will display first
    for(let i=arr.length -1; i >= 0; i--){
        showPost(arr[i]);
    }
}

//add an event listener for the 'submit' button
form.addEventListener('submit', function(e){
    e.preventDefault(); //prevents the form from being submitted by HTML by default

    let formData = new FormData(form);
    let payload = new URLSearchParams(formData); //convert FormData to URL encoded string
    
    //post the object to a server using fetch. The first argument is the endpoint
    fetch('/api/timeline_post', {
        method: "POST",
        body: payload,
    })
    .then(res => res.json())    //handle server response: extract the body of the response object and convert json to JS object
    .then(data => showPost(data))
    .catch(err => console.log(err));

    //clear the data from the form
    form.reset();
})

/*This function formats the data from fetch request, adds and displays it to the page */
showPost = jsObject =>{
    //create a div with class property = 'post'
    postDiv = document.createElement("div");
    postDiv.className = "post";

    /*create the following tags and make them children of postDiv
                -create p tags ...for name, email, postcontent, and date when post was created
    */
    namePTag = document.createElement("p");
    namePTag.appendChild(document.createTextNode("Name: " + jsObject.name));

    emailPTag = document.createElement("p");
    emailPTag.appendChild(document.createTextNode("Email: " + jsObject.email));

    postContentPTag = document.createElement("p");
    postContentPTag.appendChild(document.createTextNode("Post Content: " + jsObject.content));

    postDatePTag = document.createElement("p");
    postDatePTag.appendChild(document.createTextNode("Post Date: " + jsObject.created_at));

    postDiv.appendChild(namePTag);
    postDiv.appendChild(emailPTag);
    postDiv.appendChild(postContentPTag);
    postDiv.appendChild(postDatePTag);

    //add all the page data to the results div
    resultsTag.prepend(postDiv);
}

