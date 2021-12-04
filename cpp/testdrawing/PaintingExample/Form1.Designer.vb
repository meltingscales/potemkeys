<Global.Microsoft.VisualBasic.CompilerServices.DesignerGenerated()> _
Partial Class Form1
    Inherits System.Windows.Forms.Form

    'Form overrides dispose to clean up the component list.
    <System.Diagnostics.DebuggerNonUserCode()> _
    Protected Overrides Sub Dispose(ByVal disposing As Boolean)
        If disposing AndAlso components IsNot Nothing Then
            components.Dispose()
        End If
        MyBase.Dispose(disposing)
    End Sub

    'Required by the Windows Form Designer
    Private components As System.ComponentModel.IContainer

    'NOTE: The following procedure is required by the Windows Form Designer
    'It can be modified using the Windows Form Designer.  
    'Do not modify it using the code editor.
    <System.Diagnostics.DebuggerStepThrough()> _
    Private Sub InitializeComponent()
        Me.PictureBox1 = New System.Windows.Forms.PictureBox
        Me.Label1 = New System.Windows.Forms.Label
        Me.btnDrawSquare = New System.Windows.Forms.Button
        Me.Label2 = New System.Windows.Forms.Label
        Me.btnDrawSquareFilled = New System.Windows.Forms.Button
        Me.btnDrawCircle = New System.Windows.Forms.Button
        Me.btnDrawCircleFilled = New System.Windows.Forms.Button
        Me.Label3 = New System.Windows.Forms.Label
        Me.PictureBox2 = New System.Windows.Forms.PictureBox
        Me.Label4 = New System.Windows.Forms.Label
        CType(Me.PictureBox1, System.ComponentModel.ISupportInitialize).BeginInit()
        CType(Me.PictureBox2, System.ComponentModel.ISupportInitialize).BeginInit()
        Me.SuspendLayout()
        '
        'PictureBox1
        '
        Me.PictureBox1.Anchor = CType(((System.Windows.Forms.AnchorStyles.Top Or System.Windows.Forms.AnchorStyles.Left) _
                    Or System.Windows.Forms.AnchorStyles.Right), System.Windows.Forms.AnchorStyles)
        Me.PictureBox1.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle
        Me.PictureBox1.Location = New System.Drawing.Point(12, 25)
        Me.PictureBox1.Name = "PictureBox1"
        Me.PictureBox1.Size = New System.Drawing.Size(442, 140)
        Me.PictureBox1.TabIndex = 0
        Me.PictureBox1.TabStop = False
        '
        'Label1
        '
        Me.Label1.AutoSize = True
        Me.Label1.Location = New System.Drawing.Point(12, 9)
        Me.Label1.Name = "Label1"
        Me.Label1.Size = New System.Drawing.Size(137, 13)
        Me.Label1.TabIndex = 1
        Me.Label1.Text = "Persistent Painting Surface:"
        '
        'btnDrawSquare
        '
        Me.btnDrawSquare.Anchor = CType((System.Windows.Forms.AnchorStyles.Bottom Or System.Windows.Forms.AnchorStyles.Left), System.Windows.Forms.AnchorStyles)
        Me.btnDrawSquare.Location = New System.Drawing.Point(12, 348)
        Me.btnDrawSquare.Name = "btnDrawSquare"
        Me.btnDrawSquare.Size = New System.Drawing.Size(75, 23)
        Me.btnDrawSquare.TabIndex = 2
        Me.btnDrawSquare.Text = "Square"
        Me.btnDrawSquare.UseVisualStyleBackColor = True
        '
        'Label2
        '
        Me.Label2.Anchor = CType((System.Windows.Forms.AnchorStyles.Bottom Or System.Windows.Forms.AnchorStyles.Left), System.Windows.Forms.AnchorStyles)
        Me.Label2.AutoSize = True
        Me.Label2.Location = New System.Drawing.Point(12, 332)
        Me.Label2.Name = "Label2"
        Me.Label2.Size = New System.Drawing.Size(88, 13)
        Me.Label2.TabIndex = 3
        Me.Label2.Text = "Drawing Options:"
        '
        'btnDrawSquareFilled
        '
        Me.btnDrawSquareFilled.Anchor = CType((System.Windows.Forms.AnchorStyles.Bottom Or System.Windows.Forms.AnchorStyles.Left), System.Windows.Forms.AnchorStyles)
        Me.btnDrawSquareFilled.Location = New System.Drawing.Point(93, 348)
        Me.btnDrawSquareFilled.Name = "btnDrawSquareFilled"
        Me.btnDrawSquareFilled.Size = New System.Drawing.Size(105, 23)
        Me.btnDrawSquareFilled.TabIndex = 4
        Me.btnDrawSquareFilled.Text = "Square - Filled"
        Me.btnDrawSquareFilled.UseVisualStyleBackColor = True
        '
        'btnDrawCircle
        '
        Me.btnDrawCircle.Anchor = CType((System.Windows.Forms.AnchorStyles.Bottom Or System.Windows.Forms.AnchorStyles.Left), System.Windows.Forms.AnchorStyles)
        Me.btnDrawCircle.Location = New System.Drawing.Point(12, 377)
        Me.btnDrawCircle.Name = "btnDrawCircle"
        Me.btnDrawCircle.Size = New System.Drawing.Size(75, 23)
        Me.btnDrawCircle.TabIndex = 5
        Me.btnDrawCircle.Text = "Circle"
        Me.btnDrawCircle.UseVisualStyleBackColor = True
        '
        'btnDrawCircleFilled
        '
        Me.btnDrawCircleFilled.Anchor = CType((System.Windows.Forms.AnchorStyles.Bottom Or System.Windows.Forms.AnchorStyles.Left), System.Windows.Forms.AnchorStyles)
        Me.btnDrawCircleFilled.Location = New System.Drawing.Point(93, 377)
        Me.btnDrawCircleFilled.Name = "btnDrawCircleFilled"
        Me.btnDrawCircleFilled.Size = New System.Drawing.Size(105, 23)
        Me.btnDrawCircleFilled.TabIndex = 6
        Me.btnDrawCircleFilled.Text = "Square - Filled"
        Me.btnDrawCircleFilled.UseVisualStyleBackColor = True
        '
        'Label3
        '
        Me.Label3.AutoSize = True
        Me.Label3.Location = New System.Drawing.Point(12, 177)
        Me.Label3.Name = "Label3"
        Me.Label3.Size = New System.Drawing.Size(133, 13)
        Me.Label3.TabIndex = 7
        Me.Label3.Text = "One-time Painting Surface:"
        '
        'PictureBox2
        '
        Me.PictureBox2.Anchor = CType((((System.Windows.Forms.AnchorStyles.Top Or System.Windows.Forms.AnchorStyles.Bottom) _
                    Or System.Windows.Forms.AnchorStyles.Left) _
                    Or System.Windows.Forms.AnchorStyles.Right), System.Windows.Forms.AnchorStyles)
        Me.PictureBox2.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle
        Me.PictureBox2.Location = New System.Drawing.Point(12, 193)
        Me.PictureBox2.Name = "PictureBox2"
        Me.PictureBox2.Size = New System.Drawing.Size(442, 122)
        Me.PictureBox2.TabIndex = 8
        Me.PictureBox2.TabStop = False
        '
        'Label4
        '
        Me.Label4.Location = New System.Drawing.Point(205, 343)
        Me.Label4.Name = "Label4"
        Me.Label4.Size = New System.Drawing.Size(249, 57)
        Me.Label4.TabIndex = 9
        Me.Label4.Text = "After clicking a drawing optons button, resize the firm and move other windows in" & _
            " front of it and away again to see how the first option persists its graphics an" & _
            "d the other does not."
        Me.Label4.TextAlign = System.Drawing.ContentAlignment.MiddleLeft
        '
        'Form1
        '
        Me.AutoScaleDimensions = New System.Drawing.SizeF(6.0!, 13.0!)
        Me.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font
        Me.ClientSize = New System.Drawing.Size(466, 414)
        Me.Controls.Add(Me.Label4)
        Me.Controls.Add(Me.PictureBox2)
        Me.Controls.Add(Me.Label3)
        Me.Controls.Add(Me.btnDrawCircleFilled)
        Me.Controls.Add(Me.btnDrawCircle)
        Me.Controls.Add(Me.btnDrawSquareFilled)
        Me.Controls.Add(Me.Label2)
        Me.Controls.Add(Me.btnDrawSquare)
        Me.Controls.Add(Me.Label1)
        Me.Controls.Add(Me.PictureBox1)
        Me.MinimumSize = New System.Drawing.Size(474, 448)
        Me.Name = "Form1"
        Me.Text = "Painting Example"
        CType(Me.PictureBox1, System.ComponentModel.ISupportInitialize).EndInit()
        CType(Me.PictureBox2, System.ComponentModel.ISupportInitialize).EndInit()
        Me.ResumeLayout(False)
        Me.PerformLayout()

    End Sub
    Friend WithEvents PictureBox1 As System.Windows.Forms.PictureBox
    Friend WithEvents Label1 As System.Windows.Forms.Label
    Friend WithEvents btnDrawSquare As System.Windows.Forms.Button
    Friend WithEvents Label2 As System.Windows.Forms.Label
    Friend WithEvents btnDrawSquareFilled As System.Windows.Forms.Button
    Friend WithEvents btnDrawCircle As System.Windows.Forms.Button
    Friend WithEvents btnDrawCircleFilled As System.Windows.Forms.Button
    Friend WithEvents Label3 As System.Windows.Forms.Label
    Friend WithEvents PictureBox2 As System.Windows.Forms.PictureBox
    Friend WithEvents Label4 As System.Windows.Forms.Label

End Class
