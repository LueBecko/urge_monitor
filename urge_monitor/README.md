Issues with Psychopy



Habe doch noch weiter gesucht, und habe den Eindruck, dass der Fehler bei PsychoPy liegt. Die Fehlermeldung betraf immer ein Statement der Form: unicode(str, 'utf-8')
z.B. hier:
https://github.com/psychopy/psychopy/blob/9885bc2bdd9b024c571fd54c13da445ac140174d/psychopy/iohub/server.py#L108
 
Dieser Fehler tritt u.a. auf, wen str bereits als unicode kodiert ist. an anderen stellen wird das von PsychoPy abgefangen, z.B. hier: 
https://github.com/psychopy/psychopy/blob/9885bc2bdd9b024c571fd54c13da445ac140174d/psychopy/iohub/server.py#L77
 
Das müsste man also an der obigen Stelle auch machen (für callable_name). 
 
An anderen Stellen wird es sowohl in der per pip installierten als auch in der stand-alone Versoin falsch abgefangen (da fehlt das „not“ for dem isinstance(str, unicode)), in der aktuellen github-Version sieht es dagegen korrekt aus: 
https://github.com/psychopy/psychopy/blob/9885bc2bdd9b024c571fd54c13da445ac140174d/psychopy/iohub/server.py#L228
https://github.com/psychopy/psychopy/blob/9885bc2bdd9b024c571fd54c13da445ac140174d/psychopy/iohub/server.py#L231
 
wenn ich diese drei Stellen korrigiere (ob in der pip- oder der gebündelten Version), tritt die Fehlermeldung nicht mehr auf…
