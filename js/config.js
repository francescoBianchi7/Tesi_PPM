export class Config {
    static SERVER_URL = "http://0.0.0.0:10000/";
    static BASE_URL = `${this.SERVER_URL}`;

}
console.log('SERVER_URL=',Config.SERVER_URL)
console.log('BASE_URL=',Config.BASE_URL)
