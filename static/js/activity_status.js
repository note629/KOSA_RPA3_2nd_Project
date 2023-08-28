google.load("visualization", "1", { packages: ["corechart"] });
google.setOnLoadCallback(drawChart);

var status_btn = document.getElementById("status_btn");

status_btn.addEventListener("change", function () {
  if (this.checked) {
    console.log("checkbox가 선택되었습니다.");
    var recycle_nums = $("#recycle_nums > li").get();
    drawChart_btn(recycle_nums);
    $(".status_title").text("전체 기간 재활용품 분리수거 현황");
  } else {
    console.log("checkbox가 선택되지 않았습니다.");
    var recycle_nums = $("#month_recycle_nums > li").get();
    drawChart_btn(recycle_nums);
    $(".status_title").text("최근 1달 재활용품 분리수거 현황");
  }
});

window.addEventListener("resize", function (event) {
  if (status_btn.checked) {
    var recycle_nums = $("#recycle_nums > li").get();
    drawChart_btn(recycle_nums);
    $(".status_title").text("전체 기간 재활용품 분리수거 현황");
  } else {
    var recycle_nums = $("#month_recycle_nums > li").get();
    drawChart_btn(recycle_nums);
    $(".status_title").text("최근 1달 재활용품 분리수거 현황");
  }
  console.log("브라우저 크기가 변경되었습니다!");
});

// window.onfocus 이벤트 등록
window.onfocus = function (event) {
  if (status_btn.checked) {
    var recycle_nums = $("#recycle_nums > li").get();
    drawChart_btn(recycle_nums);
    $(".status_title").text("전체 기간 재활용품 분리수거 현황");
  } else {
    var recycle_nums = $("#month_recycle_nums > li").get();
    drawChart_btn(recycle_nums);
    $(".status_title").text("최근 1달 재활용품 분리수거 현황");
  }
  console.log("브라우저가 포커스되었습니다!");
};

function drawChart_btn(recycle_nums) {
  var max_recycle_num = 0;
  for (let i = 3; i <= 15; i++) {
    if (max_recycle_num < Number(recycle_nums[i])) {
      max_recycle_num = Number(recycle_nums[i]);
    }
  }

  var percentage = google.visualization.arrayToDataTable([
    ["Recycle Item", "Recycle Numbers"],
    ["철캔 : " + recycle_nums[3].innerHTML, Number(recycle_nums[3].innerHTML)],
    [
      "알루미늄캔 : " + recycle_nums[4].innerHTML,
      Number(recycle_nums[4].innerHTML),
    ],
    ["종이 : " + recycle_nums[5].innerHTML, Number(recycle_nums[5].innerHTML)],
    [
      "페트병(무색) : " + recycle_nums[6].innerHTML,
      Number(recycle_nums[6].innerHTML),
    ],
    [
      "페트병(유색) : " + recycle_nums[7].innerHTML,
      Number(recycle_nums[7].innerHTML),
    ],
    [
      "플라스틱(PE) : " + recycle_nums[8].innerHTML,
      Number(recycle_nums[8].innerHTML),
    ],
    [
      "플라스틱(PP) : " + recycle_nums[9].innerHTML,
      Number(recycle_nums[9].innerHTML),
    ],
    [
      "플라스틱(PS) : " + recycle_nums[10].innerHTML,
      Number(recycle_nums[10].innerHTML),
    ],
    [
      "스티로폼 : " + recycle_nums[11].innerHTML,
      Number(recycle_nums[11].innerHTML),
    ],
    [
      "비닐 : " + recycle_nums[12].innerHTML,
      Number(recycle_nums[12].innerHTML),
    ],
    [
      "유리(갈색) : " + recycle_nums[13].innerHTML,
      Number(recycle_nums[13].innerHTML),
    ],
    [
      "유리(녹색) : " + recycle_nums[14].innerHTML,
      Number(recycle_nums[14].innerHTML),
    ],
    [
      "유리(투명) : " + recycle_nums[15].innerHTML,
      Number(recycle_nums[15].innerHTML),
    ],
  ]);

  var results = google.visualization.arrayToDataTable([
    ["재활용 항목", ""],
    ["철캔", Number(recycle_nums[3].innerHTML)],
    ["알루미늄캔", Number(recycle_nums[4].innerHTML)],
    ["종이", Number(recycle_nums[5].innerHTML)],
    ["페트병(무색)", Number(recycle_nums[6].innerHTML)],
    ["페트병(유색)", Number(recycle_nums[7].innerHTML)],
    ["플라스틱(PE)", Number(recycle_nums[8].innerHTML)],
    ["플라스틱(PP)", Number(recycle_nums[9].innerHTML)],
    ["플라스틱(PS)", Number(recycle_nums[10].innerHTML)],
    ["스티로폼", Number(recycle_nums[11].innerHTML)],
    ["비닐", Number(recycle_nums[12].innerHTML)],
    ["유리(갈색)", Number(recycle_nums[13].innerHTML)],
    ["유리(녹색)", Number(recycle_nums[14].innerHTML)],
    ["유리(투명)", Number(recycle_nums[15].innerHTML)],
  ]);

  var options = {
    title: " ",
    backgroundColor: "rgb(239, 252, 235)",
    colors: [
      "cornflowerblue",
      "olivedrab",
      "orange",
      "tomato",
      "crimson",
      "purple",
      "turquoise",
      "lightseagreen",
      "lightpink",
      "gray",
      "LightSlateGray",
      "MintCream",
      "AntiqueWhite",
    ],
    pieSliceTextStyle: {
      color: "black", // 원하는 글자 색상으로 변경
    },
  };

  var opt = {
    title: " ",
    hAxis: { title: " ", titleTextStyle: { color: "red" } },
    legend: "none",
    vAxis: { minValue: 0, maxValue: max_recycle_num },
    backgroundColor: "rgb(239, 252, 235)",
    series: {
      0: {
        color: "#9400d3",
      },
    },
  };

  var chart = new google.visualization.PieChart(
    document.getElementById("piechart"),
  );
  chart.draw(percentage, options);

  var chart = new google.visualization.ColumnChart(
    document.getElementById("chart_div"),
  );
  chart.draw(results, opt);
}

function drawChart() {
  var recycle_nums = $("#month_recycle_nums > li").get();
  console.log(recycle_nums);

  var max_recycle_num = 0;
  for (let i = 3; i <= 15; i++) {
    if (max_recycle_num < Number(recycle_nums[i])) {
      max_recycle_num = Number(recycle_nums[i]);
    }
  }

  var percentage = google.visualization.arrayToDataTable([
    ["Recycle Item", "Recycle Numbers"],
    ["철캔 : " + recycle_nums[3].innerHTML, Number(recycle_nums[3].innerHTML)],
    [
      "알루미늄캔 : " + recycle_nums[4].innerHTML,
      Number(recycle_nums[4].innerHTML),
    ],
    ["종이 : " + recycle_nums[5].innerHTML, Number(recycle_nums[5].innerHTML)],
    [
      "페트병(무색) : " + recycle_nums[6].innerHTML,
      Number(recycle_nums[6].innerHTML),
    ],
    [
      "페트병(유색) : " + recycle_nums[7].innerHTML,
      Number(recycle_nums[7].innerHTML),
    ],
    [
      "플라스틱(PE) : " + recycle_nums[8].innerHTML,
      Number(recycle_nums[8].innerHTML),
    ],
    [
      "플라스틱(PP) : " + recycle_nums[9].innerHTML,
      Number(recycle_nums[9].innerHTML),
    ],
    [
      "플라스틱(PS) : " + recycle_nums[10].innerHTML,
      Number(recycle_nums[10].innerHTML),
    ],
    [
      "스티로폼 : " + recycle_nums[11].innerHTML,
      Number(recycle_nums[11].innerHTML),
    ],
    [
      "비닐 : " + recycle_nums[12].innerHTML,
      Number(recycle_nums[12].innerHTML),
    ],
    [
      "유리(갈색) : " + recycle_nums[13].innerHTML,
      Number(recycle_nums[13].innerHTML),
    ],
    [
      "유리(녹색) : " + recycle_nums[14].innerHTML,
      Number(recycle_nums[14].innerHTML),
    ],
    [
      "유리(투명) : " + recycle_nums[15].innerHTML,
      Number(recycle_nums[15].innerHTML),
    ],
  ]);

  var results = google.visualization.arrayToDataTable([
    ["재활용 항목", ""],
    ["철캔", Number(recycle_nums[3].innerHTML)],
    ["알루미늄캔", Number(recycle_nums[4].innerHTML)],
    ["종이", Number(recycle_nums[5].innerHTML)],
    ["페트병(무색)", Number(recycle_nums[6].innerHTML)],
    ["페트병(유색)", Number(recycle_nums[7].innerHTML)],
    ["플라스틱(PE)", Number(recycle_nums[8].innerHTML)],
    ["플라스틱(PP)", Number(recycle_nums[9].innerHTML)],
    ["플라스틱(PS)", Number(recycle_nums[10].innerHTML)],
    ["스티로폼", Number(recycle_nums[11].innerHTML)],
    ["비닐", Number(recycle_nums[12].innerHTML)],
    ["유리(갈색)", Number(recycle_nums[13].innerHTML)],
    ["유리(녹색)", Number(recycle_nums[14].innerHTML)],
    ["유리(투명)", Number(recycle_nums[15].innerHTML)],
  ]);

  var options = {
    title: " ",
    backgroundColor: "rgb(239, 252, 235)",
    colors: [
      "cornflowerblue",
      "olivedrab",
      "orange",
      "tomato",
      "crimson",
      "purple",
      "turquoise",
      "lightseagreen",
      "lightpink",
      "gray",
      "LightSlateGray",
      "MintCream",
      "AntiqueWhite",
    ],
    pieSliceTextStyle: {
      color: "black", // 원하는 글자 색상으로 변경
    },
  };

  var opt = {
    title: " ",
    hAxis: { title: " ", titleTextStyle: { color: "red" } },
    legend: "none",
    vAxis: { minValue: 0, maxValue: max_recycle_num },
    backgroundColor: "rgb(239, 252, 235)",
    series: {
      0: {
        color: "#9400d3",
      },
    },
  };

  var chart = new google.visualization.PieChart(
    document.getElementById("piechart"),
  );
  chart.draw(percentage, options);

  var chart = new google.visualization.ColumnChart(
    document.getElementById("chart_div"),
  );
  chart.draw(results, opt);
}
