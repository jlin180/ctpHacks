setup();
// HARD CODED
// tLink = "https://www.google.com/search?client=firefox-b-1-d&q=facebook";
// tCompany = "Facebook";
// tPosition = "SDE";
// tLocation = "New York, NY";
// tPosting = "5 days ago";
// addJobListing(tLink, tCompany, tPosition, tLocation, tPosting);

// Your web app's Firebase configuration
function setup() {
    // var firebase = require('firebase');
    var firebaseConfig = {
        apiKey: "AIzaSyDo5eHoEF5HKkvUzhZ-fFDC2QU6ahXTnU4",
        authDomain: "ctphacks.firebaseapp.com",
        databaseURL: "https://ctphacks.firebaseio.com",
        projectId: "ctphacks",
        storageBucket: "ctphacks.appspot.com",
        messagingSenderId: "549681389410",
        appId: "1:549681389410:web:2fb1e5bb1ff3359bce563b",
        measurementId: "G-WH0B8Y0W4P"
    };
    // Initialize Firebase
    firebase.initializeApp(firebaseConfig);
    firebase.analytics();
    
    var db = firebase.database();

    // console.log(db);

    var ref = db.ref('job_posts').orderByChild('datePosted');
    console.log(JSON.stringify(ref));
    ref.on('value', gotData, errData);

}

function gotData(data) {
    // console.log(JSON.stringify(data.val()));
    var jobRecord = data.val();
    var keys = Object.keys(jobRecord);
    console.log(keys);

    for (var i = 0; i < keys.length; i++) {
        var k = keys[i];
        var jlLink = jobRecord[k].link;
        var jlCompanyName = jobRecord[k].company;
        var jlPosition = jobRecord[k].title;
        var jlLocation = jobRecord[k].location;
        var jlPosting = jobRecord[k].datePosted;
        addJobListing(jlLink, jlCompanyName, jlPosition, jlLocation, jlPosting);
    }
}

function errData(err) {
    console.log('Error');
    console.log(err);
}

// jsonFormat();
// function jsonFormat() {
//     var record = '{"jobListing": [{"link": "https://www.google.com/search?client=firefox-b-1-d&q=facebook","company_name":' + 
//     ' "Facebook","position": "SDE","location": "New York, NY","posting": "5 days ago"},{"link": "https://www.google.com/search?client=firefox-b-1-d&q=amazon",' +
//     '"company_name": "Amazon","position": "Full-Stack Developer","location": "Manhattan, NY","posting": "Yesterday"},{' +
// '"link": "https://www.google.com/search?client=firefox-b-1-d&q=apple","company_name": "Apple","position": "Senior Developer","location": "New York, NY","posting": "Last week"}]}';
//     // var jsonData = JSON.parse(record);
//     // for (i = 0; i < jsonData.jobListing.length; i++) {
//     //     var record = jsonData.jobListing[i];
//     //     console.log(record.link);
//     // }
//     parseFile(record);
// }


// function getJsonFile() {
//     $.getJSON("test.json", function(json) {
//         // console.log(json);
//         parseFile(JSON.stringify(json));
//     });
// }

// Order by date?

// Parsing a JSON File into a string and pushing it into joblistings.html
function parseFile(jsonFile) {
    const jobCard = JSON.parse(jsonFile);
    for (i = 0; i < jobCard.jobListing.length; i++) {
        var jlLink = jobCard.jobListing[i].link;
        var jlCompanyName = jobCard.jobListing[i].company_name;
        // console.log(jlCompanyName);
        var jlPosition = jobCard.jobListing[i].position;
        var jlLocation = jobCard.jobListing[i].location;
        var jlPosting = jobCard.jobListing[i].posting;

        addJobListing(jlLink, jlCompanyName, jlPosition, jlLocation, jlPosting);
    }
}


// Add a job card into joblistings.html
function addJobListing(jlLink, jlCompanyName, jlPosition, jlLocation, jlPosting) {
    // var jlImg = "N/A";
    // Add jlImg to Parameters if implementing
    var jlInitial = jlCompanyName.charAt(0);
    var classColor = "google" + getClassColor(jlInitial);
    
    document.getElementById("job-listing").innerHTML += 
    '<div class="col-lg-3">' +
        '<div class="h-100 ">' +
            '<div class="jl-card card-body d-flex flex-column flex-nowrap ' + classColor + '" style="width: 100%;">' +
                '<a href="'+ jlLink + '" class="stretched-link"></a>' +
                // Image added here, if implementing
                '<div class="jl-defaultImg text-center text-nowrap mx-auto">'+ jlInitial +'<img class="rounded" src=""></div>' +
                '<div class="jl-companyName text-truncate">' + jlCompanyName + '</div>' +
                '<div class="jl-position text-truncate">' + jlPosition + '</div>' +
                '<div class="jl-location text-truncate">' + jlLocation + '</div>' +
                '<div class="jl-posting mt-auto text-right text-truncate">' + jlPosting + '</div>' +
            '</div>' +
        '</div>' +
    '</div>';
}

// Assign a color to a letter based off ASCII values
function getClassColor(str) {
    var ascii = str.charCodeAt(0);
    var classColor = "Red"; // Default
    if (ascii%4 == 0) classColor = "Red";
    else if (ascii%4 == 1) classColor = "Green";
    else if (ascii%4 == 2) classColor = "Blue";
    else classColor = "Yellow";
    return classColor;
}