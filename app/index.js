import { initializeApp } from "firebase/app";
import { firebaseConfig } from "./environment.js";
import {
  getFirestore,
  collection,
  setDoc,
  doc,
  onSnapshot,
} from "firebase/firestore";
import child_process from 'child_process';
import * as fs from 'fs';

// Initialize our firebase app connection
const app = initializeApp(firebaseConfig);
// Initialize firestore instance
const db = getFirestore(app);
console.log("initialized firebase");
const DEV_ID = "station00";

let battery0_data = ['',''];
let battery1_data = ['',''];

// Set listener to drivers on firestore
const commands_path = "/drivers/";
const commands_ref = collection(db, commands_path);
const unsub_drivers = onSnapshot(commands_ref, (snapshot) => {
  let i = 0;
  snapshot.forEach((doc_res) => {
    const driver = doc_res.data();
    console.log(driver);
    if(i == 0) {
      fs.truncateSync("/home/pi/sundo/data/drivers.csv", 0, function(){console.log('cleared driver list')});
      fs.appendFileSync("/home/pi/sundo/data/drivers.csv", `${driver.rfid},${driver.name}`)
    }else {
      fs.appendFileSync("/home/pi/sundo/data/drivers.csv", `\n${driver.rfid},${driver.name}`)
    }
    i++;
  });
});


// delay helper function
// const delay = ms => new Promise(resolve => setTimeout(resolve, ms));
async function delay(delayInms) {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve(2);
    }, delayInms);
  });
}


async function upload_battery_data(device, data) {
  const path = `/stations/${DEV_ID}/batteries/${device}`;
  const docRef = doc(db, path);
  await setDoc(docRef, data)
    .then(() => console.log("Battery",device, "updated..."))
    .catch((err) => console.log("Error:", err));
}


while(true){

  // checking for changes in Battery 1
  const new_battery0_data= child_process.execSync("tail /home/pi/sundo/data/battery0.csv -n 1").toString().split(/\r?\n/)[0].split(',');
  if(new_battery0_data[0] != battery0_data[0] && new_battery0_data[1] != battery0_data[1]) {
    console.log('uploading battery0 data')
    battery0_data  = new_battery0_data;
    upload_battery_data(0, {
      time_updated: battery0_data[0],
      level: battery0_data[1]
    })
  }

  // checking for changes in Battery 1
  const new_battery1_data= child_process.execSync("tail /home/pi/sundo/data/battery1.csv -n 1").toString().split(/\r?\n/)[0].split(',');
  if(new_battery1_data[0] != battery1_data[0] && new_battery1_data[1] != battery1_data[1]) {
    console.log('uploading battery1 data')
    battery1_data  = new_battery1_data;
    upload_battery_data(1, {
      time_updated: battery1_data[0],
      level: battery1_data[1]
    })


  }

  await delay(5000);    
  
}
  
