
var _period = 1000; // ms
var _pad = 10;
var _graph_span= 5*60;
var _dObj = {};
var _last_varlist = []

function get_data(data_cb) {
    var pullText = '';

    var since_time = Math.floor(
     ((new Date()).getTime() - _period * 3) / 1000
		     );


    xhttp = new XMLHttpRequest;
    xhttp.onreadystatechange = function() {
	if (xhttp.readyState == 4) {
            console.log('fetch_done');
	    if (xhttp.status == 200) {
                console.log('fetch was good');
                data_cb(xhttp.responseText)
	    } else {
                console.log('fetch was bad');
                data_cb('');
	    }
	}
    }
    xhttp.open('GET','/api/v1/users?since=' + since_time, true);
    xhttp.send();
}

function start_polling(period) {
    console.log('start_polling()')
    _period = period; 
    poll();
}

function poll() {
    console.log('poll()');
    get_data(arrangedata);
}

function remove_old(data,start_ts) {
    for (var ts in _dObj) {
        if (ts < start_ts) {
            delete _dObj[ts];
	}
    }
}

function copy_new(dest,src) {
 for (var ts in src) {
  dest[ts] = src[ts];
 }
}

function list_all_vars(data) {
    var vnames_hier = {}
    var varcount = 0;
    for (var time in data) {
        for (var user in data[time]) {
            for (var vname in data[time][user]) {
                if (!(user in vnames_hier)) {
                    vnames_hier[user] = {};
		}
		if (!(vname in vnames_hier[user])) {
                    vnames_hier[user][vname] = varcount++; 
		}
	    }
	}
    }

    var vnames_flat = [];
    for (var user in vnames_hier) {
        for (var vname in vnames_hier[user]) {
            vnames_flat.push(user + '__' + vname);
	}
    }
    return { 'hier': vnames_hier, 'flat': vnames_flat };
}

function arrangedata(data) {
    var d = new Date();
    var end_ts = Math.floor(d.getTime()/1000) + _pad;
    var start_ts = end_ts - _graph_span - _pad;

    remove_old(_dObj, start_ts);
    var inObj = JSON.parse(data);
    vnames_old = list_all_vars(_dObj);
    copy_new(_dObj,inObj);
    vnames_new = list_all_vars(inObj);
    vnames = list_all_vars(_dObj);
    vnames['flat'].unshift('time');

    missing_new = compare_lists(vnames_old['flat'],vnames_new['flat']).map(function(x) { return "ALERT: " + x + " has dropped." });

    document.getElementById('messages').innerHTML = missing_new.join('<br>');

    // create full sized array of nulls
    graph_data = [];
    graph_data.push(vnames['flat'])
    for (var time = start_ts; time < end_ts; time += 1) {
        var line = [];
        for (var vn in vnames['flat']) {
            line.push(null);
	}
        line[0] = (new Date(time*1000)).toLocaleTimeString();
        graph_data.push(line);
    }

    // now fill in with data, where available
    for (var ts in _dObj) {
        if ((ts >= start_ts) && (ts <= end_ts)) {
            var index = ts - start_ts + 1;
	    for (var user in _dObj[ts]) {
                for (var vn in _dObj[ts][user]) {
		    varidx = vnames['hier'][user][vn] + 1;
		    graph_data[index][varidx] = _dObj[ts][user][vn];
		}
	    }
	}
    }

    drawChart(graph_data);

    // _last_varlist = all_vars;

    setTimeout(poll, _period);
}

// returns a list of things that were in 
// l1 that were not in l2
function compare_lists(o,n) {
 var x = {}
 var r = [];
 for (var k in n) {
  x[n[k]] = 1;
 }
 for (var k in o) {
  if (!(o[k] in x)) {
   r.push(o[k]);
  } 
 }
 return r;
}

