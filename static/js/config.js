export class Config {
    static SERVER_URL = "http://127.0.0.1:5000/";
    static BASE_URL = `${this.SERVER_URL}views/`;

}
console.log('SERVER_URL=',Config.SERVER_URL)
console.log('BASE_URL=',Config.BASE_URL)