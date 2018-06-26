$(document).ready(function(){
    $('.parallax').parallax();
  });

$(document).ready(function(){
    drawChart();
    drawChart1()
});

let final=[];
let final_tags=[];
let maxpost = [];
 $.ajax({
         type: 'POST',
         url: '/graph_results',
         data: JSON.stringify(),
         contentType: 'application/json;charset=UTF-8'
     }).done(function (data) {
        console.log(data[2]);
        for(let key in data[0]){
            final.push([key, data[0][key]]);
        }
        for(let tag in data[1]){
            final_tags.push([tag,data[1][tag]]);
        }
        // document.getElementById('h2_post_title').innerHTML='Best Post of the Day'
        document.getElementById('h4_post_title').innerHTML='<b>'+data[2].post_title+'</b>';
        document.getElementById('p_category_name').innerHTML='<b>Category : </b>'+data[2].category_name;
        document.getElementById('p_uploaded_by').innerHTML='<b>Uploaded by : </b>'+data[2].email;
        document.getElementById('p_uploaded_date').innerHTML='<b>Created On : </b>'+data[2].created_date;
        // document.getElementById('img_profile').src=Flask.url_for('email_serve_image', email=post.email);
        let card_image = document.getElementById('card_image');
        let profile_image = document.createElement("img");
        document.getElementById('post_page_link').href="/post-page?post_id="+data[2].post_id;
        profile_image.src = "/img/email-serve-image?email="+data[2].email;
        profile_image.style = "width: 50%; margin-left: 25%";
        profile_image.onerror =function() {myFunction(profile_image)};
        card_image.appendChild(profile_image);
        function myFunction(profile_image) {
            profile_image.src = "https://www.tm-town.com/assets/default_male600x600-79218392a28f78af249216e097aaf683.png";
        }



    });
  // Load the Visualization API and the corechart package.
  google.charts.load('current', {'packages':['corechart']});

  // Set a callback to run when the Google Visualization API is loaded.
  google.charts.setOnLoadCallback(drawChart);
    google.charts.setOnLoadCallback(drawChart1);

  // Callback that creates and populates a data table,
  // instantiates the pie chart, passes in the data and
  // draws it.
  function drawChart() {

    // Create the data table.
     res = new google.visualization.DataTable();
    res.addColumn('string', 'Categories');
    res.addColumn('number', 'Count');
    res.addRows(final);

    // Set chart options
    var options = {'title':'',
                   'width':800,
                   'height':500};

    // Instantiate and draw our chart, passing in some options.
    var chart = new google.visualization.PieChart(document.getElementById('chart_div'));
    chart.draw(res, options);
  }

  function drawChart1() {

    // Create the data table.
    var res1 = new google.visualization.DataTable();
    res1.addColumn('string', 'Tags');
    res1.addColumn('number', 'Count');
    res1.addRows(final_tags);

    // Set chart options
    var options = {'title':'',
                    'height':800,
                    'width':500};

    // Instantiate and draw our chart, passing in some options.
    var chart = new google.visualization.PieChart(document.getElementById('chart_div_1'));
    chart.draw(res1, options);
  }
