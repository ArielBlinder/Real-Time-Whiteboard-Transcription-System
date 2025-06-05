import picture from "../Files/picture_text.png"

function UserMenual() {
    return (
        <div>
            <div>
                <br></br><h1>BoardCast</h1><br></br>
                <h3>Your tool for transcribing written text</h3>
                <br></br><p>Hello and welcome to Boardcast, here is how to use our transcribing system:</p><br></br>
                <p>First of all choose your media file whom you would like to transcribe and it's type (picture / video footage)</p>
                <p>and click on <b>"Generate Text"</b> button</p><br></br>
                <p>Then you will see your file footage dispaly on the webstie, and next to it you will see your text on a slide</p><br></br>
                <img src={picture} style={{minWidth: "70%", maxWidth:"300px"}}></img><br></br><br></br>
                <p>When chhosing a video option you will see your video footage in a media player display.</p>
                <p>and your text wriiten next to it with timestamp so you will know when was each part written</p><br></br>
                <img src={picture} style={{minWidth: "70%", maxWidth:"300px"}}></img><br></br><br></br>
                <p>All of the option let you also edit the text as your own. you can add, delete and use it however you fill like</p><br></br>
                <p>When your text is done you can have the option to export it as a docx, Pdf, txt document as you like</p><br></br>
                <p>We hope that our system will help you exceed and you will make the most out of it</p><br></br><br></br>
                <h2>Boradcast Team</h2>
            </div>
        </div>
    )
}

export default UserMenual
