const output = document.getElementById("output");
const code = document.getElementById("code");
const registers = document.getElementById("registers");
const memory = document.getElementById("memory");

function addToOutput(s) {
    output.value += ">>>" + code.value + "\n" + s + "\n";
    output.scrollTop = output.scrollHeight;
}

// Object containing functions to be exported to python
const archsim_js = {
    append_register: function(reg, val) {
        tr = document.createElement("tr")
        td1 = document.createElement("td")
        td1.innerText = "x"+reg
        td2 = document.createElement("td")
        td2.innerText = val
        td2.id = "val_x"+reg
        tr.appendChild(td1)
        tr.appendChild(td2)
        registers.appendChild(tr)
    },
    update_register: function(reg, val) {
        document.getElementById("val_x"+reg).innerText = val
    },
    append_memory: function(address, val) {
        tr = document.createElement("tr")
        td1 = document.createElement("td")
        td1.innerText = address
        td2 = document.createElement("td")
        td2.innerText = val
        td2.id = "memory"+address
        tr.appendChild(td1)
        tr.appendChild(td2)
        memory.appendChild(tr)
    },
    update_memory: function(address, val) {
        document.getElementById("memory"+address).innerText = val
    },
    append_instructions: function(cmd_json_str) {
        //setCommandString(cmd_json_str)
    }
};

output.value = "Initializing... ";
// init Pyodide
async function main() {
    let pyodide = await loadPyodide();
    await pyodide.loadPackage("micropip");
    const micropip = pyodide.pyimport("micropip");
    await micropip.install(window.location.origin+"/dist/architecture_simulator-0.1.0-py3-none-any.whl");
    pyodide.registerJsModule("archsim_js", archsim_js);
    await pyodide.runPython(`
from architecture_simulator.gui.webgui import *
sim_init()
    `);
    output.value += "Ready!\n";
    return pyodide;
}
let pyodideReadyPromise = main();

function test(){
    alert(Hello);
}

async function evaluatePython_step_sim() {
    let pyodide = await pyodideReadyPromise;
    try {
        step_sim = pyodide.globals.get("step_sim");
        let output = step_sim(cmd_json_str);
        addToOutput(output);
    } catch (err) {
        addToOutput(err);
    }
}

async function evaluatePython_run_sim(cmd_json_str) {
    let pyodide = await pyodideReadyPromise;
    try {
        run_sim = pyodide.globals.get("run_sim");
        let output = run_sim(cmd_json_str);
        addToOutput(output);
    } catch (err) {
        addToOutput(err);
    }
}
