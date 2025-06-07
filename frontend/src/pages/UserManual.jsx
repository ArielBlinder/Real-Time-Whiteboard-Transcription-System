import picture from "../Files/picture_text.png"

function UserManual() {
    return (
        <div className="user-manual-container">
            <br></br><h1 style={{color:"hsl(218, 23%, 23%);"}}>BoardCast</h1><br></br>
            <h3 style={{color:"hsl(218, 17%, 35%)"}}>Your smart tool for transcribing written text</h3>
            <br></br><p>Hello and welcome to <strong>BoardCast</strong>! here's how to use our system:</p><br></br>
            <section>
                <h4>Upload Your Media</h4>
                    <p>Start by selecting the media file you want to transcribe — either an <strong>image</strong> or a <strong>video</strong>.</p>
                    <p>Then, simply click the <b>"Generate Text"</b> button.</p><br />
                    <img src={picture} alt="Upload example" className="manual-image"></img><br /><br />
            </section>

            <section>
                <h4>View the Transcription</h4>
                <p>Your file will be displayed on the website. The system will automatically display the transcribed text next to it, in an easy-to-read format.</p>
                <p>If it's a video, it will play in an integrated media player, and the transcription will include <strong>timestamps</strong> to help you follow when each part was written.</p><br /><br />
                <img src={picture} style={{ minWidth: "70%", maxWidth: "300px" }} /><br /><br />
            </section>           

            <section>
                <h4>Edit & Export</h4>
                <p>You can also edit the transcribed text as you fit — fix mistakes, add comments, or delete unwanted parts.</p>
                <p>When you're done, you can export your work in your preferred format: <b>DOCX, PDF, or TXT</b>.</p><br /><br />
            </section>

            <h2>Boardcast Team</h2>
        </div>
    )
}

export default UserManual
