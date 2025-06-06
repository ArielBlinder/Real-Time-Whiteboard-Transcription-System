import picture from "../Files/picture_text.png"

function UserManual() {
    return (
        <div>
            <div>
                <br></br><h1>BoardCast</h1><br></br>
                <h3>Your tool for transcribing written text</h3>
                <br></br><p>Hello and welcome to Boardcast, here is how to use our transcribing system:</p><br></br>
                <p>Start by selecting the media file you want to transcribe—either an image or video.</p>
                <p>Then, simply click the <b>"Generate Text"</b> button.</p><br />
                
                <p>Your file will be displayed on the website, and the transcribed text will appear alongside it in an easy-to-read format.</p><br />
                <img src={picture} style={{minWidth: "70%", maxWidth:"300px"}}></img><br></br><br></br>

                <p>If you choose a video, it will play in an integrated media player, and the transcription will include timestamps to help you follow when each part was written.</p><br />
                <img src={picture} style={{ minWidth: "70%", maxWidth: "300px" }} /><br /><br />

                <p>You can also edit the transcribed text as you see fit—add, delete, or modify it to your liking.</p><br />

                <p>When you're done, you can export your work in your preferred format: DOCX, PDF, or TXT.</p><br />
                
                <br></br>
                <h2>Boardcast Team</h2>
            </div>
        </div>
    )
}

export default UserManual
