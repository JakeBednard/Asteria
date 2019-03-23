$( document ).ready(function() {

container = new ColorBarsContainerClass();
document.querySelector('select[name="nav-bar-routine-select"]').onchange = function(event) {
    currentRoutineRoute = event.target.value;
    container.setNextRoutine(currentRoutineRoute);
}

function ColorBarsContainerClass() {

    this.divName = 'color-bars-container';
    this.currentRoutineRoute = null;
    this.fetchWaitMilliseconds = 100;
    this.fetchInterval = null;

    this.setNextRoutine = function(nextRoutineRoute) {

        if (this.fetchInterval) {
            clearInterval(this.fetchInterval);
        }

        this.currentRoutineRoute = nextRoutineRoute;
        this.fetchRoutine();

        setInterval(this.fetchRoutine, this.fetchWaitMilliseconds);

    }

    this.fetchRoutine = function() {

        var routineResponse;

        function ajaxCall(callback){
           $.ajax({
                url: this.currentRoutineRoute,
                global: false,
                type: "GET",
                dataType: "json",
                contentType: "application/json",
                success: callback
           });
        }

        ajaxCall(routineResponse => {

            var currentColorBarDivCount =  document.getElementById('color-bars-container').childElementCount;
            var nextColorBarDivCount = routineResponse.length;

            if (nextColorBarDivCount > currentColorBarDivCount) {
                for(i=currentColorBarDivCount; i < nextColorBarDivCount; i++) {
                    var node = document.createElement("div");
                    document.getElementById('color-bars-container').appendChild(node);
                }
            }

            else if (nextColorBarDivCount < currentColorBarDivCount) {
                for(i=currentColorBarDivCount; i > nextColorBarDivCount; i--) {
                    var container = document.getElementById('color-bars-container');
                    container.removeChild(container.lastChild);
                }
            }

            console.log($("#color-bars-container > div").length);

            $("#color-bars-container > div").each(function(index, element) {

                var colorName = routineResponse[index].name;
                var colorRGB = routineResponse[index].rgb
                var transitionTime = 100
                var rgbString = 'rgb(' + colorRGB[0] + ',' + colorRGB[1] + ',' + colorRGB[2] + ')';

                console.log(rgbString);
                console.log(element);

                $(element).animate({
                    backgroundColor: rgbString
                }, transitionTime);

                //$(element).text(colorName);

            });

        })

    }

}

});