
/*
* Program för att generera uppdrag, ledtrådar, händelser och drifvaruppdrag automatiskt i form av Word-dokument.
* Skrivet av Albin Remnestål (i all (m)hast), Augusti 2016
* Vid frågor, kontakta mig på <albinre@kth.se>
*
* Lite ändrad av Toshihide Sakao Oktober 2023
* kan kontakta mig via sakao@kth.se
*/

var fs = require('fs');
var path = require('path');
var chalk = require('chalk');
var Docxtemplater = require('docxtemplater');

const emph = chalk.bold;
const ok = chalk.green;
const err = chalk.red;

_version = "20231031";

_printPath = "../Tryck-b";
_printSubDirs = ["/Uppdrag", "/Händelser", "/Drifvaruppdrag"];

// _missionPath = "../rpu/Uppdrag/";
// _eventPath = "../rpu/Händelser/";
// _drifterPath = "../rpu/Drifvaruppdrag/";

_datadir = "../../resources/rpu/data";

_missionPath =  _datadir + "/missions/";
_eventPath =  _datadir + "/events/";
_drifterPath = _datadir + "/drifters/";

var main = new function() {

    console.log("Hurry Scurry [Version " + _version + "]");
    console.log("(c) Datasektionens Mottagning");

    var arg0 = process.argv[2];
    try {
        switch (arg0) {

            case "word":

                if (!fs.existsSync(_printPath)) {
                    fs.mkdirSync(_printPath);
                }

                _printSubDirs.forEach(function(item, index) {
                    if (!fs.existsSync(_printPath + item)) {
                        fs.mkdirSync(_printPath + item);
                    }
                });

                generateMissions();
                generateEvents();
                generateDrifters();

                break;

            case undefined:
                throw new MissingArgumentError();

            default:
                throw new UnknownArgumentError(arg0);
        }
    } catch (e) {
        console.log(e.name + " : " + e.message);
    }
    console.log("Terminerar program.");
};

function generateMissions() {
    var missions = fs.readdirSync(_missionPath).filter(function(file) {
        return file != 'README.md';
    });
    var jsonDict;

    console.log("\nTillgängliga uppdrag:");
    console.log(missions);
    console.log();
    console.log("Påbörjar generering av uppdragsfiler.");

    for (var missionIndex in missions) {

        console.log(pad1(missionIndex < missions.length-1, " ") + " "
            + emph(missions[missionIndex]));

        var json = readJSON(_missionPath + missions[missionIndex]);
        var missionName = missions[missionIndex].substring(0, missions[missionIndex].length - 5);

        jsonDict = {
            "titel" : json.main.title.toUpperCase(),
            "bakgrund" : json.main.background,
            "mål" : json.main.goal,
            "belöning" : json.main.reward,
            "jakten_kan_börja" : json.main.hint
        };

        var missionDir = "../Tryck-b/Uppdrag/" + missionName;
        if (!fs.existsSync(missionDir)) {
            fs.mkdirSync(missionDir);
        }

        generateWord(jsonDict, "./mallar/Mall-uppdrag.docx", missionDir + "/" + missionName);
        console.log(pad1(true, pad2(missionIndex < missions.length-1, " ") + "   ")
                + " " + ok(missionName + ".docx"));

        var clues = json.clues;
        for (var clueIndex in clues) {
            var clueID = json.id + ":" + clues[clueIndex].id;
            var clueID_verbose = json.id + "_ledtråd_" + clues[clueIndex].id;
            jsonDict = {
                "id" : clueID,
                "titel" : json.main.title.toUpperCase(),
                "text" : clues[clueIndex].text
            };

            var clueDir = missionDir + "/ledtrådar";
            if (!fs.existsSync(clueDir)) {
                fs.mkdirSync(clueDir);
            }

            generateWord(jsonDict, "./mallar/Mall-ledtrådar.docx", clueDir + "/" + clueID_verbose);
            console.log(pad1(clueIndex < clues.length-1, pad2(missionIndex < missions.length-1, " ") + "   ")
                + " " + ok(clueID_verbose + ".docx"));
        }
    };
}

function generateEvents() {

    var generalEventDir = "../Tryck-b/Händelser";
    if (!fs.existsSync(generalEventDir)) {
        fs.mkdirSync(generalEventDir);
    }

    console.log("\nPåbörjar generering av händelsefiler.");

    // generateFor("Positiva", true);
    // generateFor("Negativa", false);

    generateFor("positive", true);
    generateFor("negative", false);

    function generateFor(eventType, padding) {

        var eventDir = generalEventDir + "/" + eventType;
        if (!fs.existsSync(eventDir)) {
            fs.mkdirSync(eventDir);
        }

        console.log(pad1(padding, " ") + " " + emph(eventType + " händelser"));

        var events = readJSON(_eventPath + eventType + ".json").events;
        var jsonDict;

        for (var eventIndex in events) {

            jsonDict = {
                "titel" : events[eventIndex].title.toUpperCase(),
                "text" : events[eventIndex].text
            };

            var fileName = events[eventIndex].title.split(" ").join("_");
            generateWord(jsonDict, "./mallar/Mall-händelser.docx", eventDir + "/" + fileName);
            console.log(pad1(eventIndex < events.length-1, pad2(padding, " ") + "   ")
                + " " + ok(fileName + ".docx"));
        }

    }

};

function generateDrifters() {

    var drifters = readJSON(_drifterPath + "/hitta.json").missions;
    var jsonDict;

    console.log("\nPåbörjar generering av drifvaruppdragsfiler.");

    var drifterDir = "../Tryck-b/Drifvaruppdrag";
    if (!fs.existsSync(drifterDir)) {
        fs.mkdirSync(drifterDir);
    }

    for (var drifterIndex in drifters) {

        jsonDict = {
            "namn" : drifters[drifterIndex].name.toUpperCase(),
            "goal" : drifters[drifterIndex].goal
        };
        generateWord(jsonDict, "./mallar/Mall-drifvare.docx", drifterDir + "/" + "hitta" + drifterIndex);
        console.log(pad1(drifterIndex < drifters.length-1, " ") + " " + ok(drifters[drifterIndex].id + ".docx"));

    };
};

function generateWord(jsonDict, templatePath, destinationPath){

    //Load the docx file as a binary
    var template = fs.readFileSync(templatePath, "binary");
    var doc = new Docxtemplater(template);

    doc.setData(jsonDict);
    doc.render();

    var buf = doc.getZip().generate({type:"nodebuffer"});

    fs.writeFileSync(destinationPath + ".docx", buf);
};

function pad1(bool, padding) {
    return padding + (bool ? "+" : "`") + "----";
    //return padding + (bool ? "\u251C" : "\u2514") + "\u2500".repeat(3);
};

function pad2(bool, padding) {
    return padding + (bool ? "|" : " ");
    //return padding + (bool ? "\u2502" : " ");
};

function getFiles(srcPath) {
    return fs.readdirSync(srcPath).filter(function(file) {
        return !fs.statSync(path.join(srcPath, file)).isDirectory();
    }).filter(function(file) {
        return file != 'desktop.ini';
    });
};

function getDirectories(srcPath) {
    return fs.readdirSync(srcPath).filter(function(file) {
        return fs.statSync(path.join(srcPath, file)).isDirectory();
    });
};

function readJSON(file) {
    var content = fs.readFileSync(file, 'utf8');
    var jsonContent = JSON.parse(content);
    // console.log(jsonContent);
    return jsonContent;
};

function MissingArgumentError(message) {
    this.name = "MissingArgumentError";
    this.message = message || "Additional arguments expected";
    this.stack = (new Error()).stack;
};

function UnknownArgumentError(arg) {
    this.name = "UnknownArgumentError";
    this.message = "Could not recognize argument " + arg;
    this.stack = (new Error()).stack;
};
