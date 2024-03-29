//Global vars (oher than data and metadata)
const years = Object.keys(data);
const meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio",
    "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"];
const tooltipData = { "Principal": {}, "porMeses": {}, "Año": {} };
var dtchart;
var ycchart;
var yschart;
var firstYear = metadata["firstYear"];
var lastYear = metadata["lastYear"];

document.getElementById("title1").innerHTML = "Estaci&oacute;n: <b>" + metadata["indicativo"] + "</b>     , " + metadata["nombre"] + ", " + metadata["provincia"];
document.getElementById("title2").innerHTML = "Altitud " + metadata["altitud"] + "m."
document.getElementById("lastedyears").innerHTML = "Promedio años " + firstYear + "-" + lastYear;
var closeModal = document.getElementsByClassName("close")[0];
var modalWindow = document.getElementById("details");
var yearRangeFirst = document.getElementById("yearRangeFirst");
var yearRangeLast = document.getElementById("yearRangeLast");

for (y in years) {
    opt1 = document.createElement("option");
    opt1.value = years[y]; opt1.innerHTML = years[y];
    if (y == 0)
        opt1.selected = true;
    opt2 = document.createElement("option");
    opt2.value = years[y]; opt2.innerHTML = years[y];
    if (y == years.length - 1)
        opt2.selected = true;
    document.getElementById("firstYear").appendChild(opt1)
    document.getElementById("lastYear").appendChild(opt2);
}

closeModal.onclick = function () {
    modalWindow.style.display = "none";
}
window.onclick = function (event) {
    if (event.target == modalWindow) {
        modalWindow.style.display = "none";
    }
}

yearRangeFirst.onchange = function () {
    firstYear = yearRangeFirst.value;
    document.getElementById("lastedyears").innerHTML = "Promedio años " + firstYear + "-" + lastYear;
    yearCollection(firstYear, lastYear);
    yearSummary(firstYear, lastYear);
}

yearRangeLast.onchange = function () {
    lastYear = yearRangeLast.value;
    document.getElementById("lastedyears").innerHTML = "Promedio años " + firstYear + "-" + lastYear;
    yearCollection(firstYear, lastYear);
    yearSummary(firstYear, lastYear);
}

yearCollection(firstYear, lastYear);
yearSummary(firstYear, lastYear);

function yearCollection(first, last) {
    precTotal = []; tMed = []; absMax = []; absMin = []; dlluvia = [];
    //Resumen por años
    for (i = years.indexOf(first); i < years.indexOf(last) + 1; i++) {
        prec = 0;
        tmed = 0;
        aMax = -100;
        aMin = 100;
        dl = 0;
        rd = 0;
        rdd = "";
        yeardata = data[years[i]];
        months = Object.keys(yeardata);
        numMonths = 0;
        for (j in months) {
            numMonths += 1;
            prec = prec + yeardata[months[j]]["totalPrec"];
            dl = dl + yeardata[months[j]]["rainyDays"];
            tmed = tmed + yeardata[months[j]]["tMed"]
            if (yeardata[months[j]]["tMax"] > aMax)
                aMax = yeardata[months[j]]["tMax"];
            if (yeardata[months[j]]["tMin"] < aMin)
                aMin = yeardata[months[j]]["tMin"];
            if (yeardata[months[j]]["rainiestDay"]["prec"] > rd) {
                rd = yeardata[months[j]]["rainiestDay"]["prec"];
                rdd = yeardata[months[j]]["rainiestDay"]["day"];
            }
        }
        tMed.push(tmed / numMonths);
        precTotal.push(prec);
        fecha = [meses[parseInt(rdd.split("-")[1])], rdd.split("-")[2]];
        dlluvia.push("\nDias con lluvia: " + dl + "\nDia mas lluvioso " + fecha[1] + " "
            + fecha[0] + "  " + rd + " mm");
        absMax.push(aMax);
        absMin.push(aMin);
    }

    if (ycchart != undefined)
        ycchart.destroy();

    tooltipData["Principal"] = { "Precipitacion": dlluvia };
    ycchart = drawChart('consolidated', "Principal",
        years.slice(years.indexOf(first), years.indexOf(last) + 1),
        [['line', 'Temp Media', tMed], ['line', 'Max Absoluta', absMax],
        ['line', 'Min Absoluta', absMin], ['bar', 'Precipitacion', precTotal]]);
}

function yearSummary(first, last) {
    //Resumen por meses
    mtMax = []; mtMaxMed = []; mtMin = []; mtMinMed = []
    mtMed = []; mtotalPrec = []; mrainyDays = []; myMaxAbs = []; myMinAbs = [];
    tprec = 0; trainydays = 0;
    tabsMax = []; tabsMin = [];
    maxMed = -100; mmaxMed = "";
    minMed = 100; mminMed = "";

    for (m in meses) {
        tp = tmaxm = tminm = tmed = rd = 0;
        absMax = -100; iyMax = 0;
        absMin = 100; iyMin = 0;
        count = 0;
        mes = parseInt(m)
        for (i = years.indexOf(first); i < years.indexOf(last) + 1; i++) {
            yeardata = data[years[i]];
            if (yeardata[mes + 1] != undefined) { //El mes existe
                tp = tp + yeardata[mes + 1]["totalPrec"];
                tmaxm = tmaxm + yeardata[mes + 1]["tMaxMed"];
                tminm = tminm + yeardata[mes + 1]["tMinMed"];
                tmed = tmed + yeardata[mes + 1]["tMed"];
                rd = rd + yeardata[mes + 1]["rainyDays"];
                if (yeardata[mes + 1]["tMax"] > absMax) {
                    absMax = yeardata[mes + 1]["tMax"];
                    iyMax = i;
                }
                if (yeardata[mes + 1]["tMin"] < absMin) {
                    absMin = yeardata[mes + 1]["tMin"];
                    iyMin = i
                }
                count += 1;
            }
        }

        mtotalPrec.push(tp / count);
        tprec = tprec + (tp / count);
        mtMaxMed.push(tmaxm / count);
        tabsMax.push(absMax); tabsMin.push(absMin);

        if ((tmaxm / count) > maxMed) {
            maxMed = (tmaxm / count);
            mmaxMed = m;
        }
        mtMinMed.push(tminm / count);
        if ((tminm / count) < minMed) {
            minMed = (tminm / count);
            mminMed = m;
        }
        mtMed.push(tmed / count);
        mrainyDays.push("\nPromedio días lluviosos " + Math.round(rd / count));
        trainydays += Math.round(rd / count);
        myMaxAbs.push("\nAño Máxima: " + years[iyMax]);
        myMinAbs.push("\nAño Mínima: " + years[iyMin]);
    }

    tooltipData["porMeses"] = {
        "Precipitación": mrainyDays, "Máxima Absoluta": myMaxAbs,
        "Mínima Absoluta": myMinAbs
    };

    document.getElementById("lydetails").innerHTML = "Precipitación anual promedio en el periodo <b>"
        + Number(tprec).toFixed(2) + "</b> mm" +
        "<br>Promedio de d&iacute;as lluviosos anuales en el periodo: <b>" + trainydays + "</b>" +
        "<br>Mes mas caluroso <b>" + meses[mmaxMed] + "</b> con máxima promedio "
        + Number(maxMed).toFixed(1) + " C" +
        "<br>Mes más frío <b>" + meses[mminMed] + "</b> con mínima promedio "
        + Number(minMed).toFixed(1) + " C";

    if (yschart != undefined)
        yschart.destroy();

    yschart = drawChart("chartmonths", "porMeses", meses,
        [["line", "Temp. Media", mtMed], ["bar", "Precipitación", mtotalPrec],
        ['line', "Máxima Media", mtMaxMed], ['line', 'Mínima Media', mtMinMed],
        ['point', 'Máxima Absoluta', tabsMax], ['point', 'Mínima Absoluta', tabsMin]]);
}

function singleYear(year) {
    tMax = []; tMin = []; tMaxMed = []; tMinMed = []; totalPrec = []; mrDays = []
    tabsMax = {}; tabsMin = {}
    tYearPrec = rainyDays = 0
    absMax = -100
    absMin = 100
    yearData = data[parseInt(year)];

    for (m in yearData) {
        tMax.push(yearData[m]["tMax"]);
        tMin.push(yearData[m]["tMin"]);
        tMaxMed.push(yearData[m]["tMaxMed"]);
        tMinMed.push(yearData[m]["tMinMed"]);
        totalPrec.push(yearData[m]["totalPrec"]);
        tYearPrec = tYearPrec + yearData[m]["totalPrec"];
        rainyDays = rainyDays + yearData[m]["rainyDays"];
        mrDays.push("\nDías con lluvia :" + yearData[m]["rainyDays"]);
    }

    tooltipData["Año"] = { "Precipitación": mrDays };

    document.getElementById("ydetails").innerHTML = "Precipitación anual total <b>"
        + tYearPrec.toFixed(2) + "</b> mm" +
        "<br>Dias con lluvia <b>" + rainyDays;

    if (dtchart != undefined)
        dtchart.destroy();

    dtchart = drawChart("detailYear", "Año", meses,
        [['line', 'Temp Max', tMax], ['line', 'Temp. Min', tMin],
        ['line', 'Max Media', tMaxMed], ['line', "Min Media", tMinMed],
        ['bar', "Precipitación", totalPrec]]);

}


function drawChart(canvasid, title, labels, charts) {
    cx = document.getElementById(canvasid);
    ds = [];
    for (i in charts) {
        if (charts[i][0] == 'line') {
            ds.push({
                type: "line",
                yAxisID: 'y1',
                label: charts[i][1],
                data: charts[i][2],
                borderWidth: 2
            });
        };
        if (charts[i][0] == 'bar') {
            ds.push({
                type: "bar",
                yAxisID: 'y2',
                label: charts[i][1],
                data: charts[i][2]
            });
        };
        if (charts[i][0] == 'point') {
            ds.push({
                type: "line",
                yAxisID: 'y1',
                label: charts[i][1],
                data: charts[i][2],
                showLine: false,
                fill: false,
                pointRadius: 5
            });
        };
    }

    ch = new Chart(cx, {
        data: {
            labels: labels,
            datasets: ds
        },
        options: {
            maintainAspectRatio: true,
            scales: {
                y1: {
                    position: 'left',
                    stacked: false,
                    title: { text: "Grados C", display: true },
                    suggestedMin: 0,
                    suggestedMax: 50
                },
                y2: {
                    position: 'right',
                    stacked: false,
                    title: { text: "mm", display: true },
                    suggestedMin: 0
                }
            },
            plugins: {
                title: {
                    display: false,
                    text: title
                },
                tooltip: {
                    callbacks: {
                        afterBody: function (x) {
                            lab = x[0].label;
                            chtitle = x[0].chart.titleBlock.options.text;
                            chdata = x[0].dataset.label;
                            (isNaN(lab) ? idx = meses.indexOf(lab) : idx = parseInt(lab) - parseInt(firstYear))
                            if (tooltipData[chtitle][chdata] != undefined) {
                                text = tooltipData[chtitle][chdata][idx];
                                return text;
                            } else
                                return;
                        }
                    }
                }
            },
            onClick: function (e, activeEls) {
                let dataIndex = activeEls[0].index;
                let label = e.chart.data.labels[dataIndex];
                if (isNaN(label))
                    return;
                else {
                    document.getElementById("details").style.display = "block";
                    document.getElementById("year").innerHTML = "Resumen del a&ntilde;o " + label;
                    singleYear(label);
                }
            }
        }
    });
    //console.log("Chart = " + ch);
    return ch;
}
