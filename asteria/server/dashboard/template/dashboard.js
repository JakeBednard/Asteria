window.addEventListener("load", function() {

    container = new ColorBarsContainerClass();
    document.querySelector('select[name="nav-bar-routine-select"]').onchange = function(event) {
        currentRoutineRoute = event.target.value;
        container.setNextRoutine(currentRoutineRoute);
    }

function ColorBarsContainerClass() {

    this.divName = 'color-bars-container';
    this.currentRoutineRoute = null;
    this.fps = 2;
    this.fetchWaitMilliseconds = 1000;
    this.colorBars = [];
    this.fetchInterval = null;
    this.drawInterval = null;

    this.setNextRoutine = function(nextRoutineRoute) {

        this.currentRoutineRoute = nextRoutineRoute;
        this.fetchRoutine();

    }

    this.fetchRoutine = function() {

        if (this.fetchInterval) {
            clearInterval(this.fetchInterval);
        }

        xhttp = new XMLHttpRequest();

        xhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                response = JSON.parse(this.responseText);
                window.container.setupRoutine(response);
            }
            else if (this.readyState == 4 && this.status != 200) {
                console.log("Server Error: Could not fetch color at API endpoint: " + currentRoutineRoute);
            }
            else {
                // Ahh the request is still processing... I think?
                // Because not readyState 4.
            }
        };

        xhttp.open("GET", currentRoutineRoute, true);
        xhttp.send();

    }

    this.setupRoutine = function(routineResponse) {

        if (this.drawInterval) {
            clearInterval(this.drawInterval);
        }

        if (this.colorBars.length < routineResponse.length) {
            for(i=this.colorBars.length; i < routineResponse.length; i++) {
                this.colorBars.push(new ColorBarClass());
            }
        }
        else if (this.colorBars.length > routineResponse.length) {
            for(i=this.colorBars.length; i > routineResponse.length; i--) {
                this.colorBars.pop();
            }
        }

        for(i=0; i < this.colorBars.length; i++) {
            this.colorBars[i].setNextColor(
                routineResponse[i].name,
                routineResponse[i].rgb,
                1000,
                this.fps
            )
        }

        this.fetchInterval = setInterval(this.fetchRoutine, this.fetchWaitMilliseconds);
        this.drawInterval = setInterval(this.draw, (1/this.fps));

    }

    this.draw = function() {

        var currentColorBarDivCount =  document.getElementById(this.divName).childElementCount;

        if (this.colorBars < currentColorBarDivCount) {
            for(i=this.colorBars.length; i < currentColorBarDivCount; i++) {
                var node = document.createElement("div");
                document.getElementById(this.divName).appendChild(node);
            }
        }

        else if (this.colorBars > currentColorBarDivCount) {
            for(i=this.colorBars.length; i > routineResponse.length; i--) {
                var container = document.getElementById(this.divName);
                container.removeChild(container.lastChild);
            }
        }

        for(i=0; i < this.colorBars.length; i++) {
            var div = document.querySelector(".content a:nth-child(" + i + ")");
            div.style.backgroundColor = this.colorBars[i].rgbString();
        }

    }

}

function ColorBarClass() {

    this.currentColorName = 'None';
    this.currentRGB = [0,0,0];
    this.destinationRGB = [0,0,0];
    this.colorStepDeltas = [0,0,0];
    this.updateInterval = null;

    this.setNextColor = function(colorName, nextRGB, tweenDurationMilliseconds, fps) {

        this.currentColorName = colorName;
        this.destinationRGB = nextRGB;

        var totalFrames = tweenDurationMilliseconds / 1000 * fps;
        var msPerFrame = tweenDurationMilliseconds / totalFrames;

        if (this.updateInterval) {
            clearInterval(this.updateInterval);
        }

        // Calculate Color Delta Step Per Frame for Tweening
        for(i=0; i<3; i++) {

            var current = this.currentRGB[i];
            var destination = this.destinationRGB[i];

            var totalDelta = destination - current;
            var stepDelta = totalDelta / totalFrames;

            this.colorStepDeltas[i] = stepDelta;

        }

        this.updateInterval = setInterval(this.step, msPerFrame);

        return;

    }

    this.step = function() {

        // Figure out next color per step and if destination has already been reached.
        for(i=0; i<3; i++) {

            current = this.currentRGB[i];
            destination = this.destinationRGB[i];
            delta = this.colorStepDeltas[i];

            if (delta > 0) {
                if (current < destination) {
                    this.currentRGB[i] += delta;
                }
            }

            else if (delta < 0) {
                if (current > destination) {
                    this.currentRGB[i] += delta;
                }
            }

        }

        return;

    }

    /*
    this.asHTMLString = function() {

        return `
        <p>
            <strong>Color Name:</strong> ${this.currentColorName} <br>
            <strong>Current RGB:</strong> (${this.currentRGB[0]},${this.currentRGB[1]},${this.currentRGB[2]}) <br>
            <strong>Destination RGB:</strong> (${this.destinationRGB[0]},${this.destinationRGB[1]},${this.destinationRGB[2]})
        </p>
        `;

    }
    */

    this.rgbString = function() {
        return "rgb(" + this.currentRGB[0] + ", " + this.currentRGB[1] + ", " + this.currentRGB[2] + ")";
    }

}

});