import react, { useState, useEffect, useMemo, useRef } from 'react';
import Spinner from '../layout/Spinner';
import { Document, Packer, Paragraph, TextRun } from "docx";
import { saveAs } from "file-saver";
import { jsPDF } from "jspdf";
import { FaPen, FaSave, FaFileAlt, FaFileWord, FaFilePdf } from "react-icons/fa"

function FileOuputSegment({ inputOption, file, showFile, generatedText, isLoading }) {

    const [text, setText] = useState(generatedText || "");
    const [isEditing, setIsEditing] = useState(false);


    const videoUrl = useMemo(() => {
        return file ? URL.createObjectURL(file) : null;
    }, [file]);


    useEffect(() => {
        return () => {
            if (videoUrl) {
                URL.revokeObjectURL(videoUrl);
            }
        };
    }, [videoUrl]);


    useEffect(() => {
        setText(generatedText || "");
    }, [generatedText]);


    // Helper function to remove timestamps from text for export
    const removeTimestamps = (textContent) => {
        // Remove timestamps in format [h:mm:ss] or [m:ss] 
        return textContent.replace(/\[\d{1,2}:\d{2}:\d{2}\]\s*/g, '').trim();
    };

    const handleExportToTxt = () => {
        const cleanText = removeTimestamps(text);
        const doc = new Blob([cleanText], { type: 'text/plain' });
        saveAs(doc, "transcription.txt")
    }


    const handleExportToDocx = () => {
        const cleanText = removeTimestamps(text);
        const paragraphs = cleanText.split('\n').map(line =>
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
        const cleanText = removeTimestamps(text);
        const doc = new jsPDF();
        const lines = doc.splitTextToSize(cleanText, 180);

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
                    {file && showFile && inputOption === "video" && (<video controls className='responsive-media' src={videoUrl} type="video/mp4"></video>)}
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
                                <div className="resizable-box">
                                    {isEditing ? (
                                        <textarea className='editable-textarea' value={text} onChange={(e) => setText(e.target.value)} rows={15}></textarea>
                                    ) : (<p id='text'>{text}</p>
                                    )}
                                </div>
                            </section>
                        </div>
                        <div className='download-buttons-container'>
                            <button className='download-buttons' onClick={handleExportToTxt}>
                                <FaFileAlt size={12} style={{ marginRight: "5px" }} />
                                Download as .txt
                            </button>
                            <button className='download-buttons' onClick={handleExportToDocx}>
                                <FaFileWord size={12} style={{ marginRight: "5px" }} />
                                Download as .docx
                            </button>
                            <button className='download-buttons' onClick={handleExportToPDF}>
                                <FaFilePdf size={12} style={{ marginRight: "5px" }} />
                                Download as PDF
                            </button>
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

export default FileOuputSegment