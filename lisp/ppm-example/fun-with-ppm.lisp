(load "util.lisp")

; Q: Dafuq is a PPM?
; A: It's a super simple image format.
;
; See http://netpbm.sourceforge.net/doc/ppm.html
;
; For example, a PPM of: BLACK WHITE
;                        WHITE BLACK
;
; Would look like:
;
; +----coolimage.ppm----+
; | P3                  | 
; | 2 2                 |
; | 16                  |
; | 0  0  0   15 15 15  |
; | 15 15 15  0  0  0   |
; +---------------------+


;Magic number for a PPM.
(defvar magic-number "P3")

(defclass Pixel ()
  (
    (red    :initarg :red     :initform 0   :type integer)
    (green  :initarg :green   :initform 0   :type integer)
    (blue   :initarg :blue    :initform 0   :type integer)
  )
)

(defun PIXEL-BLACK  () (make-instance 'Pixel :red 0  :green 0  :blue 0 ))
(defun PIXEL-WHITE  () (make-instance 'Pixel :red 15 :green 15 :blue 15))
(defun PIXEL-RED    () (make-instance 'Pixel :red 15 :green 0  :blue 0 ))
(defun PIXEL-GREEN  () (make-instance 'Pixel :red 0  :green 15 :blue 0 ))
(defun PIXEL-BLUE   () (make-instance 'Pixel :red 0  :green 0  :blue 15))

(defun distance2d (x1 y1 x2 y2) (sqrt (+ (square (- x2 x1)) 
                                         (square (- y2 y1)))))
;; Sanity check for distance2d.
(if (not (= (distance2d 0 0 3 0) 3))        (error "0,0 and 0,3 should be 3 away from eachother!") )
(if (not (= (distance2d 0 0 1 1) (sqrt 2))) (error "0,0 and 1,1 should be sqrt(2) away from eachother!") )

(defmethod pixel-data ((thing Pixel))
"Get the data from a Pixel object.
This is generally just three ASCII numbers,
i.e. a black pixel's 'data' is '0 0 0'."

  (concatenate 'string
    (pixel-value-to-string (slot-value thing 'red))
    (pixel-value-to-string (slot-value thing 'green))
    (pixel-value-to-string (slot-value thing 'blue))
  )
)

(defun pixel-value-to-string (pixel-value) 
  (format nil "~3,'0@<~d~>" pixel-value) 
  ; Left-aligned, three long digits.
)

(defclass PPM ()
  (
    (magic-number :initarg :magic-number  :initform magic-number    :type string)
    (width        :initarg :width         :initform 3               :type integer)
    (height       :initarg :height        :initform 3               :type integer)
    (depth        :initarg :depth         :initform 16              :type integer)
    (pixels       :initarg :pixels        :initform 
      ; A 3x3 grid of black pixels.
      (loop for y from 1 to 3 collect
        (loop for x from 1 to 3 collect
          (PIXEL-BLACK)))
                                                                    :type list)
  )
  
  (:documentation
    "A class representing a PPM image.
    It has a width, a height, and a 2d array of pixels, among other things."
    )
  )

(defun pixel-grid-generate-rectangle (width height) 
"Generate a grid of Pixel objects that looks like a rectangle."
  (loop for y from 1 to height collect 
    (loop for x from 1 to width collect 
      
      (cond 
          ; If y or x are on the edges,
          ((or
            (= y 1) (= y height) 
            (= x 1) (= x width))
            ; Give 'em an edge pixel.
            (PIXEL-BLUE)) 
         
          ; All other conditions,
         (t 
           ; Give 'em an inside pixel.
           (PIXEL-RED))
      )
    )
  )
)

(defun pixel-grid-generate-circle (radius) 
"Generate a grid of Pixel objects that looks like a circle."
  (loop for y from (- (- radius 1)) to radius collect ; y ∈ [-radius, radius]
    (loop for x from (- (- radius 1)) to radius collect ; x ∈ [-radius, radius]
      
      (cond
       
       ; If (x,y) distance from center is less than radius,
       ((< (distance2d x y 0 0) radius )
       ; Give 'em an inside pixel.
       (PIXEL-BLUE))

        ; All other conditions,
        (t 
        ; Give 'em an outside pixel.
        (PIXEL-RED))
      )
    )
  )
)

(defun random-pixel (&optional (depth 16))
  (make-instance 'Pixel :red (random depth) :green (random depth) :blue (random depth) )
)

(defun pixel-grid-data (grid)
"Get the data from a 2d pixel grid.
Generally looks like this:

0  0  0   15 15 15
15 15 15  0  0  0 "
  (format nil "~{~a~^~%~}" ; Separate each row of pixels by a newline.
    (loop for col in grid collect ; For all columns,
      (format nil "~{~a~^ ~}" ; Separate each pixel-data in our row by spaces. 
        (loop for pixel in col collect ; For all pixels,
          (pixel-data pixel) ; Get the pixel's RGB separated by spaces.
        )
      )
    )
  )
)

(defmethod ppm-data ((thing PPM))
  "Get the data from a PPM object.
  This can be written to a file and viewed by IrfanView or some other PPM viewer."
  (format nil 
"~$
~D ~D
~D
~$"
    (slot-value thing 'magic-number)
    (slot-value thing 'width) (slot-value thing 'height)
    (slot-value thing 'depth)
    (pixel-grid-data (slot-value thing 'pixels))
  )
)

(defmethod write-ppm-to-file ((thing PPM) (filename string))
"Write a PPM object to a file."
  (with-open-file 
    (s filename :direction :output :if-exists :supersede) ; 's' is the filestream.
    (format s "~$" (ppm-data thing)) ; Here, instead of printing to stdout, we print to 's'.
  )
)

(format t "Below, we can see a simple Pixel object.~%")
(defvar cool-pixel (make-instance 'Pixel :green 4 :blue 5))
(describe cool-pixel)
(format t "Notice that 'red' is 0 because I set an :initform for it in the Pixel constructor.~%")
(newline 2)

(format t "Hm... I wonder if green is still 4...~%")
(format t "We can access a specific property by using slot-value below:~%")
(format t "Green of cool-pixel is '~S'" (slot-value cool-pixel 'green))
(newline 2)

(format t "What would our pixel look like if it were in a PPM file?~%")
(princ (pixel-data cool-pixel))
(newline 2)

(format t "Now, let's try making a default PPM object...")
(defvar cool-ppm (make-instance 'PPM))
(describe cool-ppm)
(newline 2)

(format t "To mix things up, let's make the middle pixel a pink one!~%")
(describe (slot-value cool-ppm 'pixels))
(setf
  (nth 1 (nth 1 (slot-value cool-ppm 'pixels))) ; At 1,1 aka the middle
  (make-instance 'Pixel :red 15 :blue 15 :green 3)) ; New pink pixel

(format t "Here's the data that our default PPM object has.
This should be a 3x3 of black pixels with a pink one in the middle:~%~%")
(format t "~$~%~%" (ppm-data cool-ppm))
(format t "Let's write this to a PPM file called '3x3black.PPM'.~%")
(write-ppm-to-file cool-ppm "3x3black.PPM")
(format t "Done!~%~%")

(format t "Now, let's make a 12x5 rectangle.~%")
(defvar rect-ppm (make-instance 'PPM 
  :width 12
  :height 5
  :pixels (pixel-grid-generate-rectangle 12 5))
)
(describe rect-ppm)
(format t "Let's see how that grid looks. It'll be at 'rectangle.ppm'.")
(write-ppm-to-file rect-ppm "rectangle.ppm")


(format t "Finally, let's make a 50x50 circle.~%")
(defvar circ-ppm (make-instance 'PPM 
  :width 50
  :height 50
  :pixels (pixel-grid-generate-circle 25)) ; Note how we pass a radius of 25 but our circle is 50x50.
)
(describe circ-ppm)
(format t "Let's see how that circle looks. It'll be at 'circle.ppm'.")
(write-ppm-to-file circ-ppm "circle.ppm")
