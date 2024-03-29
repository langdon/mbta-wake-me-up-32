function startWakeTimer(train_id, station, wake_time) {
	wake_time = moment(wake_time);
	wake_time.subtract('m', 5); // subtract some buffer
	
	alert("will wake you up at " + wake_time.local().format("M/d/YYYY HH:mm") + " which is 5 minutes before arrival");
	
}

function trainChosen(train_id, station) {
	// /<system>/<line>/<trip>/<station>
	$.getJSON('/mbta/red/'+ train_id + "/" + station, function(data) {
  		var items = [];

		$("#directions").html("Now where do you want to wake up?");
		
		$.each(data, function(index, trip_obj) {
			//<li class="ui-widget-content" train-id="1">Item 1</li>
    		items.push('<li class="ui-widget-content" train-id="'+ trip_obj.Trip + '"' +
    			'station-id="' + trip_obj.PlatformKey + '"' +
    			'wake-time="' + trip_obj.Time + '">' + 
    			trip_obj.StationName  + '</li>');
  		});

		$('#selectable').html(items.join(''));

		$( "#selectable" ).selectable({
			selected: function(event, ui) {
				if ($(".ui-selected").length > 0) {
					var selected_item = $(".ui-selected").first();
					startWakeTimer(selected_item.attr("train-id"), 
						selected_item.attr("station-id"),
						selected_item.attr("wake-time"));
				}
			}
		});

	});
}


function getTrains(station) {
	if (station == undefined ) {
		station = 'RDTCN'
	}
	$.getJSON('/mbta/red/'+ station + '/trains', function(data) {
  		var items = [];

		$.each(data, function(index, trip_obj) {
			//<li class="ui-widget-content" train-id="1">Item 1</li>
    		items.push('<li class="ui-widget-content" train-id="'+ trip_obj.Trip +'">' + trip_obj.StationName + 
    			" Train #" + trip_obj.Trip + '</li>');
  		});

		$('#selectable').html(items.join(''));

		$( "#selectable" ).selectable({
			selected: function(event, ui) {
				if ($(".ui-selected").length > 0) {
					trainChosen($(".ui-selected").first().attr("train-id"));
				}
			}
		});
	});
/*	
	$.get('/route/' + line + '/trains', function(data) {
		for ()
	})
*/
}

$(function() {
	getTrains();
	//
});
