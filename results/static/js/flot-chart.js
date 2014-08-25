/**
 * Created by ankesh on 4/7/14.
 */
var options = {
    series: {
        color: "#FFFFFF",
        lines:{
            show: false,
            color: "#b32c44"
        },
        points:{
            show: false
        },
         bars: { show: true,
            fill: true,
            fillColor: "#B32C44",
            horizontal: false,
            barWidth: 0.3,
            align: "center"
        }
    },

    axisLabels: {
            show: true
        },

    xaxis:{
        mode: "categories",
        axisLabel: "Image Name",
        axisLabelUseCanvas: true,
        axisLabelFontFamily: "'Lato', sans-serif",
        axisLabelFontSizePixels: 12,
        axisLabelColour: "#ffffff",
        font:{
            color: "#EFEFF2",
            family: "'Lato', sans-serif"
        },
        axisLabelPadding: 10,
        autoscaleMargin: 0.1
    },

    yaxis:{
        mode: "",
        font:{
            family: "'Lato', sans-serif",
            color: "#EFEFF2"
        },
        axisLabel: "Absolute Rays per second",
        axisLabelUseCanvas: true,
        axisLabelFontFamily: "'Lato', sans-serif",
        axisLabelFontSizePixels: 12,
        axisLabelColour: "#ffffff",
        axisLabelPadding: 5
    },
    grid:{
        //backgroundColor: "#3d3d3d",
        color: "#B6B6B9",
        hoverable: true,
        margin: 10
    },
    tooltip: true,
    tooltipOpts: {
        content: "%x | %y",
        defaultTheme: false
    }
};

    var data = [{}];