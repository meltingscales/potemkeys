Imports System.Environment

Public Class frmMain
    Dim stringFont As Font
    Dim string_format As New StringFormat()

    Dim my_WinName As String
    Const my_WinStatic As String = " ver. "
    Dim my_WinVersion As String
    Dim my_WinRelease As String
    Dim my_WinBuild As String
    Dim my_WinSubBuild As String
    Dim my_Delim1 As String
    Dim emb_Delim1 As Boolean
    Dim my_Delim2 As String
    Dim emb_Delim2 As Boolean
    Dim txt_Display_Ver As String
    Dim txt_Curr_Build As String
    Dim txt_UBR_Value As String
    Dim the_File As String
    Dim version_Complete As Boolean
    Dim current_Ver As String
    Dim previous_Ver As String

    Private Sub Form1_Load(sender As Object, e As EventArgs) Handles MyBase.Load
        Try
            If My.Settings.UpgradeRequired = True Then
                My.Settings.Upgrade()
                My.Settings.UpgradeRequired = False
                My.Settings.Save()
            End If
        Catch ex As Exception
            MessageBox.Show(ex.Message, "Upgrade from Previous Version Error")
        End Try

        conMenuAbout.Text = My.Application.Info.AssemblyName & "  (ver. " & My.Application.Info.Version.ToString & ")"
        prop_Grid.SelectedObject = My.Settings

        string_format.Alignment = StringAlignment.Far
        string_format.LineAlignment = StringAlignment.Near

        version_Complete = False

        form_Defaults()

        Me.WindowState = FormWindowState.Minimized

        nextTime.Interval = 500
        nextTime.Start()
    End Sub

    Private Sub nextTime_Tick(sender As Object, e As EventArgs) Handles nextTime.Tick
        Dim d As Graphics = Graphics.FromHwnd(IntPtr.Zero)

        Dim brush_Name As System.Drawing.Brush = New System.Drawing.SolidBrush(My.Settings.color_Win_Name)
        Dim brush_Static As System.Drawing.Brush = New System.Drawing.SolidBrush(My.Settings.color_static_Ver)
        Dim brush_WinVer As System.Drawing.Brush = New System.Drawing.SolidBrush(My.Settings.color_Win_Version)
        Dim brush_CharDelim As System.Drawing.Brush = New System.Drawing.SolidBrush(My.Settings.color_Char_Delim)
        Dim brush_Curr_Rel As System.Drawing.Brush = New System.Drawing.SolidBrush(My.Settings.color_Curr_Release)
        Dim brush_Curr_Bld As System.Drawing.Brush = New System.Drawing.SolidBrush(My.Settings.color_Curr_Build)
        Dim brush_UBR_Delim As System.Drawing.Brush = New System.Drawing.SolidBrush(My.Settings.color_UBR_Delim)
        Dim brush_UBR_Rev As System.Drawing.Brush = New System.Drawing.SolidBrush(My.Settings.color_UpdateBldRev)

        update_Version()

        Dim writeHere As New PointF(Screen.PrimaryScreen.Bounds.Right - 300, Screen.PrimaryScreen.Bounds.Bottom - 64)
        d.DrawString(my_WinName, stringFont, brush_Name, writeHere)

        writeHere.X += d.MeasureString(my_WinName, stringFont).Width - My.Settings.Space_1
        d.DrawString(my_WinStatic, stringFont, brush_Static, writeHere)

        writeHere.X += d.MeasureString(my_WinStatic, stringFont).Width - My.Settings.Space_2
        d.DrawString(my_WinVersion, stringFont, brush_WinVer, writeHere)

        writeHere.X += d.MeasureString(my_WinVersion, stringFont).Width - My.Settings.Space_3
        d.DrawString(my_Delim1, stringFont, brush_CharDelim, writeHere)

        writeHere.X += d.MeasureString(my_Delim1, stringFont).Width - My.Settings.Space_4
        d.DrawString(my_WinRelease, stringFont, brush_Curr_Rel, writeHere)

        writeHere.X += d.MeasureString(my_WinRelease, stringFont).Width - My.Settings.Space_5
        d.DrawString(my_Delim1, stringFont, brush_CharDelim, writeHere)

        writeHere.X += d.MeasureString(my_Delim1, stringFont).Width - My.Settings.Space_6
        d.DrawString(my_WinBuild, stringFont, brush_Curr_Bld, writeHere)

        writeHere.X += d.MeasureString(my_WinBuild, stringFont).Width - My.Settings.Space_7
        d.DrawString(my_Delim2, stringFont, brush_UBR_Delim, writeHere)

        writeHere.X += d.MeasureString(my_Delim2, stringFont).Width - My.Settings.Space_8
        d.DrawString(my_WinSubBuild, stringFont, brush_UBR_Rev, writeHere)

    End Sub

    Public Sub form_Defaults()

        Try
            nextTime.Interval = My.Settings.updateInterval
            Me.Opacity = My.Settings.Opacity / 100
            my_Delim1 = My.Settings.char_Delimiter
            emb_Delim1 = My.Settings.embolden_Char_Delim
            my_Delim2 = My.Settings.UBR_Delimiter
            emb_Delim2 = My.Settings.embolden_UBR_Char
        Catch ex As Exception
            MessageBox.Show(ex.Message)
        End Try

        update_Version()

        If current_Ver <> previous_Ver Then
            Try
                If Not String.IsNullOrEmpty(My.Settings.text_Version_File) Then
                    the_File = My.Settings.text_Version_File
                Else
                    ofd.FileName = "WinVer.txt"
                    If ofd.ShowDialog = DialogResult.OK Then
                        My.Settings.text_Version_File = ofd.FileName
                        the_File = ofd.FileName
                    End If
                End If
            Catch ex As Exception
                Dim str_Err = ex.Message
                ofd.FileName = "WinVer.txt"
                If ofd.ShowDialog = DialogResult.OK Then
                    My.Settings.text_Version_File = ofd.FileName
                    the_File = ofd.FileName
                End If
            End Try
            conMenuSaveVer_Click(Nothing, Nothing)
            previous_Ver = current_Ver
        End If

    End Sub

    Private Sub update_Version()
        Try
            Dim tmpStr As String = My.Computer.Registry.GetValue("HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion", "ProductName", Nothing)
            my_WinName = Replace(tmpStr, "Windows ", "Win ")
            tmpStr = Replace(my_WinName, "Professional", "Pro")
            my_WinName = Replace(tmpStr, "Enterprise", "Pro")
            my_WinVersion = My.Computer.Registry.GetValue("HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion", "CurrentVersion", Nothing)
            my_WinRelease = My.Computer.Registry.GetValue("HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion", "DisplayVersion", Nothing)
            my_WinBuild = My.Computer.Registry.GetValue("HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion", "CurrentBuild", Nothing)
            Dim myKey As Microsoft.Win32.RegistryKey = Microsoft.Win32.RegistryKey.OpenBaseKey(Microsoft.Win32.RegistryHive.LocalMachine, Microsoft.Win32.RegistryView.Registry64)
            Dim myKey2 As Object = myKey.OpenSubKey("SOFTWARE\Microsoft\Windows NT\CurrentVersion")
            Dim myVal As Int64 = Convert.ToInt64(myKey2.GetValue("UBR").ToString)
            my_WinSubBuild = myVal
            current_Ver = my_WinName & my_WinVersion & my_WinRelease & my_WinBuild & my_WinSubBuild
            stringFont = New Font(My.Settings.useFont, My.Settings.useFont.Style)
            version_Complete = True
        Catch ex As Exception
            MessageBox.Show(ex.Message)
        End Try
    End Sub

    Private Sub conMenuExit_Click(sender As Object, e As EventArgs) Handles conMenuExit.Click
        Application.Exit()
    End Sub

    Private Sub conMenuSettings_Click(sender As Object, e As EventArgs) Handles conMenuSettings.Click
        Me.WindowState = FormWindowState.Normal
    End Sub

    Private Sub frmMain_Resize(sender As Object, e As EventArgs) Handles MyBase.Resize
        If Me.WindowState = FormWindowState.Minimized Then
            Me.sysTrayIcon.Visible = True
            Me.ShowInTaskbar = False
        Else
            Me.ShowInTaskbar = True
            Me.sysTrayIcon.Visible = False
        End If
    End Sub

    Private Sub frmMain_FormClosing(sender As Object, e As FormClosingEventArgs) Handles MyBase.FormClosing
        e.Cancel = True
        Me.WindowState = FormWindowState.Minimized
    End Sub

    Private Sub conMenuSaveVer_Click(sender As Object, e As EventArgs) Handles conMenuSaveVer.Click
        If version_Complete = False Then
            Exit Sub
        End If

        Try
            My.Computer.FileSystem.WriteAllText(the_File, current_Ver, False)
        Catch ex As Exception
            MessageBox.Show(Me, ex.Message, "Save Version Error")
        End Try

        Try
            If Not String.IsNullOrEmpty(current_Ver) Then
                If Not String.IsNullOrWhiteSpace(current_Ver) Then
                    Clipboard.SetText(current_Ver)
                End If
            End If
        Catch ex As Exception
            MessageBox.Show(Me, ex.Message, "Clipboard Error")
        End Try
    End Sub

End Class
