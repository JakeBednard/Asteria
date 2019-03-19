window.addEventListener("load", function() {

    var data_refresh_wait_ms = 200;
    var screen_refresh_wait_ms = 41;

    var canvas;
    var context;

    var red = 0;
    var green = 0;
    var blue = 0;

    var dx_red = 0;
    var dx_green = 0;
    var dx_blue = 0;
    var dx_time = data_refresh_wait_ms / screen_refresh_wait_ms;

    function main() {
        canvas = document.getElementById('canvas');
        context = canvas.getContext('2d');
        resizeCanvas();
        window.addEventListener('resize', resizeCanvas, false);
        setInterval(refreshCanvasBackgroundColor, data_refresh_wait_ms);
        setInterval(transitionCanvasBackgroundColor, screen_refresh_wait_ms);
    }

    function resizeCanvas() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight - document.getElementById("top-bar").height;
    }

    function refreshCanvasBackgroundColor() {

        xhttp = new XMLHttpRequest();

        xhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                jsonResponse = JSON.parse(this.responseText);
                console.log(jsonResponse[0]);
                setNextColor(jsonResponse[0]);
            }
            else {
                console.log("Could not reach API Endpoint.")
            }
        };
        xhttp.open("GET", "api/airplane_mode", true);
        xhttp.send();

    }

    function setNextColor(next_color) {

        var red_difference = colorDistance(red, next_color.red);
        var green_difference = colorDistance(green, next_color.green);
        var blue_difference = colorDistance(blue, next_color.blue);

        dx_red = red_difference/dx_time;
        dx_green = green_difference/dx_time;
        dx_blue = blue_difference/dx_time;

    }

    function colorDistance(originalColor, newColor) {

        var distance = 0;

        if (originalColor > newColor) {
            distance = -1 * (originalColor - newColor);
        }
        else {
            distance = newColor - originalColor;
        }

        return distance;

    }

    function transitionCanvasBackgroundColor() {

        red = red + dx_red;
        green = green + dx_green;
        blue = blue + dx_blue;

        context.fillStyle = make_rgb_string(red, green, blue);
        context.fillRect(0, 0, canvas.width, canvas.height);
        context.drawImage(canvas, 0, 0);

    }

    function make_rgb_string(r, g, b) {
        return "rgb(" + r + ", " + g + ", " + b + ")";
    }

    main();

})
