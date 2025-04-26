import react, {useState, useEffect} from 'react';
import Spinner from '../layout/Spinner';
import { Document, Packer, Paragraph, TextRun } from "docx";
import { saveAs } from "file-saver";
import { jsPDF } from "jspdf";
import { FaPen, FaSave, FaFileAlt, FaFileWord, FaFilePdf } from "react-icons/fa"

function FileOutputUI({ inputOption, file, showFile, generatedText, isLoading}) {

    const [text, setText] = useState(generatedText || "");
    const [isEditing, setIsEditing] = useState(false);


    useEffect(() => {
        setText(generatedText || "");
    }, [generatedText]);


    const handleExportToTxt = () => {
        const doc = new Blob([text], {type: 'text/plain'});
        saveAs(doc,"transcription.txt")
    }


    const handleExportToDocx = () => {
        const paragraphs = text.split('\n').map(line =>
            new Paragraph({
                children: [new TextRun(line)],
            })
        );
    
        const doc = new Document({
            sections: [
                {
                    children: paragraphs,
                },
            ],
        });
    
        Packer.toBlob(doc).then(blob => {
            saveAs(blob, "transcription.docx");
        });
    };


    const handleExportToPDF = () => {
        const doc = new jsPDF();
        const lines = doc.splitTextToSize(text, 180);
    
        doc.text(lines, 10, 10);
        doc.save("transcription.pdf");
    }

    const toggleEdit = () => {
        setIsEditing((prev) => !prev);
    };
    


    return (
        <>
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
                            <section id='text-area'>
                                <button className='edit-button' onClick={toggleEdit}>
                                    {isEditing ? <FaSave size={20} /> : <FaPen size={20} />}
                                </button>
                                {isEditing ? (
                                    <textarea className='editable-textarea' value={text} onChange={(e) => setText(e.target.value)} rows={8}></textarea>
                                ) : (<p id='text'>{text}</p>
                                )}
                            </section>
                        </div>
                        <div className='download-buttons-container'>
                        <button className='download-buttons' onClick={handleExportToTxt}>
                        <FaFileAlt size={12} style={{ marginRight: "px" }} />
                        Download as .txt
                         </button>
                            <button className='download-buttons' onClick={handleExportToDocx}>Download as .docx</button>
                            <button className='download-buttons' onClick={handleExportToPDF}>Download as PDF</button>
                        </div>
                    </div>)}
            </div>
            <div>
                {isLoading && (
                    <Spinner></Spinner>
                )}
            </div>
        </>
    );


}

export default FileOutputUI