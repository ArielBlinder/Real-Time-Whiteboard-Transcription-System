import react, {useState} from 'react';

function FileOutputUI({ inputOption, file, showFile, text}) {



    const handleDownloadText = (format) => {
        console.log(`Download as ${format}`);


    };


    return (
        <div className='output-container'>
            <div className='media-output-container'>
                {file && showFile && inputOption === "video" && (<video controls className='responsive-media' src={URL.createObjectURL(file)} type="video/mp4"></video>)}
                {file && showFile && inputOption === "image" && (<img className='responsive-media' src={URL.createObjectURL(file)} ></img>)}
            </div>
            {file && showFile && (
                <div className='generated-text'>
                    <div className='generated-text-container'>
                        <div className='generated-text-header'>
                            Generated Text
                        </div>
                        <section>
                            <p id='text'>{text}</p>
                        </section>
                    </div>
                    <div className='download-buttons-container'>
                        <button className='download-buttons' onClick={handleDownloadText("txt")}>download as .txt</button>
                        <button className='download-buttons' onClick={handleDownloadText("docx")}>download as .docx</button>
                        <button className='download-buttons' onClick={handleDownloadText("PDF")}>download as PDF</button>
                    </div>
                </div>)}
        </div>
    );


}

export default FileOutputUI