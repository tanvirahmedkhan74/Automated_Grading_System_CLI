import spawnCommand from "spawn-command"

export const backendServer = () => {
    try {
        process.chdir('../server');
        const sc = spawnCommand('npm run dev');
        console.log('Back-end Server Started Successfully!');
    } catch (error) {
        console.log('Error while Starting the server.js');
    }
}

export const llmServer = () => {
    try {
        process.chdir('../LLM/ml-server');
        const sc = spawnCommand('uvicorn main:app --port 5000');
        
    } catch (error) {
        console.log('Error while Starting the fastApi Server');
    }
}