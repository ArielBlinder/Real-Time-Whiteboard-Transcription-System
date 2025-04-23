import react, {useState} from 'react';

function FileOutputUI({ inputOption, file, showFile}) {

    //const text = "DurDuring the 1984–85 English football season, Gillingham F.C. competed in the Football League Third Division, the third tier of the English football league system. It was the 53rd season in which Gillingham competed in the Football League, and the 35th since the club was voted back into the league in 1950. Gillingham started the Third Division season with five wins in the first seven games and were challenging for a place in the top three of the league table, which would result in promotion to the Second Division. The team's performances then declined, culminating in a 7–1 defeat to York City in November which left them in mid-table. They then won 12 out of 16 games to go back up to second place, before a poor run in March meant that they again dropped out of the promotion places. Gillingham finished the season fourth in the table, missing promotion by one place.ing Gillingham F.C.'s 1984–85 season, they competed in the Football League Third Division, the third tier of the English football league system. It was the 53rd season in which Gillingham competed in the Football League, and the 35th since they were voted back into the league in 1950. Gillingham started the season with five wins in the first seven games and were challenging for a place in the top three of the league table, which would result in promotion to the Second Division. Gillingham also competed in three knock-out competitions, reaching the fourth round of the FA Cup and the second round of the Football League Cup but losing in the first round of the Associate Members' Cup. The team played 56 competitive matches, winning 30, drawing 9, and losing 17. Tony Cascarino was the club's leading goalscorer, scoring 20 goals in all competitions. Keith Oakes made the most appearances, playing 54 times. The highest attendance recorded at the club's home ground, Priestfield Stadium, was 8,881 for a League Cup game against Leeds United in September.";
    const text = `Syllabus:
(1) DEs (7-8 lectures) : ordinary diff. equations (ODEs). partial diff. equations (PDES)
(2) Line & double integrals : arclengths of curves (3 lectures) areas
(3) Calculus of functions in two variables : Surfaces, gradients, Taylor's Thu critical pts, Lagrange multipliers`



    const handleDownloadText = (format) => {
        console.log(`Download as ${format}`);


    };


    return (
        <div className='output-container'>
            <div className='media-output-container'>
                {file && showFile && inputOption === "video" && (<video controls className='responsive-media' src={file} type="video/mp4"></video>)}
                {file && showFile && inputOption === "image" && (<img className='responsive-media' src={file} ></img>)}
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