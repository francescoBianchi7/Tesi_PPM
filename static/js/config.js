export class Config {
    static SERVER_URL = "http://127.0.0.1:5000";
    static BASE_URL = `${this.SERVER_URL}`;
    static TEMP_URL = "http://0.0.0.0:10000"
}
//const SCRIPT_ROOT = {{ request.script_root|tojson }}
//console.log('SCRIPT_ROOT', SCRIPT_ROOT)
console.log('TEMP_URL',Config.TEMP_URL)
console.log('SERVER_URL=',Config.SERVER_URL)
console.log('BASE_URL=',Config.BASE_URL)

tracking.ColorTracker.registerColor('green', function(r, g, b) {
  return r < 50 && g > 200 && b < 50;
});
tracking.ColorTracker.registerColor('black', function(r, g, b) {
  return r < 40 && g < 40 && b < 40;
});