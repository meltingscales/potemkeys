Public Class Form1

    Private Enum DrawOptions
        None
        Square
        SquareFilled
        Circle
        CircleFilled
    End Enum

    ' this variable contains the drawing instructions. In a production application, 
    ' this would probably be replaced with co-ordinates, colors, line thicknesses, and 
    ' other more specific drawing instructions. This is just for example purposes...
    Private m_eDrawOptions As DrawOptions = DrawOptions.None

    Private Sub Form1_Load(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles MyBase.Load
        PictureBox1.Padding = New Padding(25)
        PictureBox2.Padding = New Padding(25)
    End Sub

    Private Sub PictureBox1_Resize(ByVal sender As Object, ByVal e As System.EventArgs) Handles PictureBox1.Resize
        ' this prevents artifacts during a resize...
        PictureBox1.Invalidate()
    End Sub

    ''' <summary>
    ''' All of the painting is done in this event. Instructions are stored 
    ''' at the module level, and used to draw on the surface every time the
    ''' PictureBox is invalidated.
    ''' </summary>
    Private Sub PictureBox1_Paint(ByVal sender As System.Object, ByVal e As System.Windows.Forms.PaintEventArgs) Handles PictureBox1.Paint
        Me.PaintPicturebox(m_eDrawOptions, PictureBox1, e.Graphics)
        ' NOTE: because we are in the Paint event for the control, and the Graphics object
        ' was passed to us as a parameter, we do not need to Dispose it when we are finished.
        ' Any time you use a drawing surface's CreateGraphics method to obtain an instance
        ' of a surface's Graphics object, however, you must call Dispose on it when you are
        ' through using it, or else you will end up with significant memory innefficiencies
        ' in your application...
    End Sub

    Private Sub PaintPicturebox(ByVal DrawOptions As DrawOptions, ByVal Surface As PictureBox, ByVal Graphics As Graphics)
        ' get the rectangle that we will be working with...
        Dim clsBounds As New Rectangle(Surface.Padding.Left, _
            Surface.Padding.Top, _
            Surface.Width - (Surface.Padding.Left + Surface.Padding.Right), _
            Surface.Height - (Surface.Padding.Top + Surface.Padding.Bottom))
        ' evaluate instructions and draw accordingly...
        Select Case DrawOptions
            Case DrawOptions.Square
                Graphics.DrawRectangle(Pens.Blue, clsBounds)
            Case DrawOptions.SquareFilled
                Graphics.DrawRectangle(Pens.Blue, clsBounds)
                Graphics.FillRectangle(Brushes.SteelBlue, clsBounds)
            Case DrawOptions.Circle
                Graphics.DrawEllipse(Pens.Red, clsBounds)
            Case DrawOptions.CircleFilled
                Graphics.DrawEllipse(Pens.Red, clsBounds)
                Graphics.FillEllipse(Brushes.Salmon, clsBounds)
            Case Else
                ' draw nothing...
        End Select
    End Sub

    Private Sub btnDrawSquare_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles btnDrawSquare.Click
        ' store the drawing instructions...
        m_eDrawOptions = DrawOptions.Square
        ' instruct the PictureBox that it is time to redraw itself - this
        ' is the same message sent to the control when it is made visible,
        ' either the first time or after a window is placed over it and 
        ' then removed. It triggers the Paint event.
        PictureBox1.Invalidate()
        ' draw one time onto the other picturebox to illustrate how 
        ' it is not persistent...
        Dim clsGraphics As System.Drawing.Graphics = PictureBox2.CreateGraphics()
        PaintPicturebox(DrawOptions.Square, PictureBox2, clsGraphics)
        clsGraphics.Dispose() ' NOTE: this line is important for resource management...
    End Sub

    Private Sub btnDrawSquareFilled_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles btnDrawSquareFilled.Click
        ' store the drawing instructions...
        m_eDrawOptions = DrawOptions.SquareFilled
        ' instruct the PictureBox that it is time to redraw itself - this
        ' is the same message sent to the control when it is made visible,
        ' either the first time or after a window is placed over it and 
        ' then removed. It triggers the Paint event.
        PictureBox1.Invalidate()
        ' draw one time onto the other picturebox to illustrate how 
        ' it is not persistent...
        Dim clsGraphics As System.Drawing.Graphics = PictureBox2.CreateGraphics()
        PaintPicturebox(DrawOptions.SquareFilled, PictureBox2, clsGraphics)
        clsGraphics.Dispose() ' NOTE: this line is important for resource management...
    End Sub

    Private Sub btnDrawCircle_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles btnDrawCircle.Click
        ' store the drawing instructions...
        m_eDrawOptions = DrawOptions.Circle
        ' instruct the PictureBox that it is time to redraw itself - this
        ' is the same message sent to the control when it is made visible,
        ' either the first time or after a window is placed over it and 
        ' then removed. It triggers the Paint event.
        PictureBox1.Invalidate()
        ' draw one time onto the other picturebox to illustrate how 
        ' it is not persistent...
        Dim clsGraphics As System.Drawing.Graphics = PictureBox2.CreateGraphics()
        PaintPicturebox(DrawOptions.Circle, PictureBox2, clsGraphics)
        clsGraphics.Dispose() ' NOTE: this line is important for resource management...
    End Sub

    Private Sub btnDrawCircleFilled_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles btnDrawCircleFilled.Click
        ' store the drawing instructions...
        m_eDrawOptions = DrawOptions.CircleFilled
        ' instruct the PictureBox that it is time to redraw itself - this
        ' is the same message sent to the control when it is made visible,
        ' either the first time or after a window is placed over it and 
        ' then removed. It triggers the Paint event.
        PictureBox1.Invalidate()
        ' draw one time onto the other picturebox to illustrate how 
        ' it is not persistent...
        Dim clsGraphics As System.Drawing.Graphics = PictureBox2.CreateGraphics()
        PaintPicturebox(DrawOptions.CircleFilled, PictureBox2, clsGraphics)
        clsGraphics.Dispose() ' NOTE: this line is important for resource management...
    End Sub

End Class
