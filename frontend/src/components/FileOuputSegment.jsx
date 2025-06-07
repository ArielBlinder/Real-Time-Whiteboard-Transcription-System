import react, { useState, useEffect, useMemo, useRef } from 'react';
import Spinner from '../layout/Spinner';
import { Document, Packer, Paragraph, TextRun } from "docx";
import { saveAs } from "file-saver";
import { jsPDF } from "jspdf";
import { FaPen, FaSave, FaFileAlt, FaFileWord, FaFilePdf } from "react-icons/fa"

function FileOuputSegment({ inputOption, file, showFile, generatedText, isLoading }) {

    const [text, setText] = useState(generatedText || "");
    const [isEditing, setIsEditing] = useState(false);
    const [currentTime, setCurrentTime] = useState(0);
    const videoRef = useRef(null);


    // store the video URL so it wil be created only once
    const videoUrl = useMemo(() => {
        return file ? URL.createObjectURL(file) : null;
    }, [file]);


    // revokes the URL when the component unmounts
    useEffect(() => {
        return () => {
            if (videoUrl) {
                URL.revokeObjectURL(videoUrl);
            }
        };
    }, [videoUrl]);

    // sets the generated text as text
    useEffect(() => {
        setText(generatedText || "");
    }, [generatedText]);

     // Parse timestamps and text segments
     const textSegments = useMemo(() => {
        if (!text) return [];
        
        // Split by timestamp pattern and keep the timestamps
        const parts = text.split(/(\[\d{1,2}:\d{2}:\d{2}\])/);
        const segments = [];
        
        for (let i = 0; i < parts.length; i++) {
            const part = parts[i];
            
            // Check if this part is a timestamp
            const timestampMatch = part.match(/\[(\d{1,2}):(\d{2}):(\d{2})\]/);
            if (timestampMatch) {
                const hours = parseInt(timestampMatch[1]);
                const minutes = parseInt(timestampMatch[2]);
                const seconds = parseInt(timestampMatch[3]);
                const timeInSeconds = hours * 3600 + minutes * 60 + seconds;
                
                // Get the text that follows this timestamp
                const followingText = parts[i + 1] || "";
                
                segments.push({
                    timestamp: part,
                    timeInSeconds,
                    text: followingText,
                    fullSegment: part + followingText
                });
            }
        }
        
        return segments;
    }, [text]);


     // Find the active segment based on current video time
     const activeSegmentIndex = useMemo(() => {
        if (textSegments.length === 0)
            return -1;
        
        let activeIndex = -1;
        for (let i = 0; i < textSegments.length; i++) {
            if (currentTime >= textSegments[i].timeInSeconds) {
                activeIndex = i;
            } else {
                break;
            }
        }
        
        return activeIndex;
    }, [textSegments, currentTime]);


     // Handle video time update
     const handleTimeUpdate = () => {
        if (videoRef.current) {
            setCurrentTime(videoRef.current.currentTime);
        }
    };


    // Handle clicking on a timestamp to get to thqt time in the video  
    const handleTimestampClick = (timeInSeconds) => {
        if (videoRef.current) {
            videoRef.current.currentTime = timeInSeconds
        }  
    }


    // Helper function to remove timestamps from text for export
    const removeTimestamps = (textContent) => {
        // Remove timestamps in format [h:mm:ss] or [m:ss] 
        return textContent.replace(/\[\d{1,2}:\d{2}:\d{2}\]\s*/g, '').trim();
    };


    // handle downloading the text as a txt file
    const handleExportToTxt = () => {
        const cleanText = removeTimestamps(text);
        const doc = new Blob([cleanText], { type: 'text/plain' });
        saveAs(doc, "transcription.txt")
    }

    
    // handle downloading the text as a docx file
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

    // handle downloading the text as a pdf file
    const handleExportToPDF = () => {
        const cleanText = removeTimestamps(text);
        const doc = new jsPDF();
        const lines = doc.splitTextToSize(cleanText, 180);

        doc.text(lines, 10, 10);
        doc.save("transcription.pdf");
    }

    // change the state of the edit from new edit to save
    const toggleEdit = () => {
        setIsEditing((prev) => !prev);
    };


    return (
        <>
            <div className='output-container'>
                <div className='media-output-container'>
                    {file && showFile && inputOption === "video" && (<video ref={videoRef} controls className='responsive-media' src={videoUrl} type="video/mp4" onTimeUpdate={handleTimeUpdate}></video>)}
                    {file && showFile && inputOption === "image" && (<img className='responsive-media' src={URL.createObjectURL(file)} ></img>)}
                </div>
                {file && showFile && (
                    <div className='generated-text'>
                        <div className='generated-text-container'>
                            <div className='generated-text-header'>
                                Generated Text
                            </div>
                            <section id='text-area'>
                                <button className='edit-button' onClick={toggleEdit} title={`Click to ${isEditing ? 'save edited text' : 'edit text'}`}>
                                    {isEditing ? <FaSave size={20} /> : <FaPen size={20} />}
                                </button>
                                <div className="resizable-box">
                                    {isEditing ? (
                                        <textarea className='editable-textarea' value={text} onChange={(e) => setText(e.target.value)} rows={15}></textarea>
                                    ) : ( 
                                    <div id='text'>
                                         {textSegments.length > 0 ? (
                                            textSegments.map((segment, index) => (
                                                <span key={index} className={`text-segment ${index === activeSegmentIndex ? 'active' : ''}`}>
                                                    <span className="timestamp" onClick={() => handleTimestampClick(segment.timeInSeconds)} title="Click to jump to this time">
                                                        {segment.timestamp}
                                                    </span>
                                                    {segment.text}
                                                </span>
                                            ))
                                        ) : (
                                            <p>{text}</p>
                                        )}
                                    </div>
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