import { app, BrowserWindow, ipcMain } from 'electron'
import path from 'path'
import { spawn, ChildProcess } from 'child_process'
import fs from 'fs'
import { fileURLToPath } from 'url'

const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)

let mainWindow: BrowserWindow | null = null
let backendProcess: ChildProcess | null = null

const startBackend = () => {
  // In production, the backend executable will be bundled
  const isDev = !app.isPackaged
  const backendPath = isDev 
    ? path.join(__dirname, '../../backend/venv/Scripts/python.exe')
    : path.join(process.resourcesPath, 'backend', 'backend.exe')

  const backendArgs = isDev 
    ? ['-m', 'uvicorn', 'main:app', '--reload', '--port', '8000']
    : []

  const backendOptions = {
    cwd: isDev ? path.join(__dirname, '../../backend') : process.resourcesPath,
    stdio: 'pipe' as const
  }

  if (!isDev && !fs.existsSync(backendPath)) {
    console.error(`Backend executable not found at ${backendPath}`)
    return
  }

  backendProcess = spawn(backendPath, backendArgs, backendOptions)

  backendProcess.stdout?.on('data', (data) => {
    console.log(`Backend: ${data}`)
  })

  backendProcess.stderr?.on('data', (data) => {
    console.error(`Backend Error: ${data}`)
  })
}

const createWindow = () => {
  const appIconPath = process.env.VITE_DEV_SERVER_URL
    ? path.join(__dirname, '../../frontend/public/icon.ico')
    : path.join(__dirname, '../dist/icon.ico');

  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    icon: appIconPath,
    title: 'LocalMind',
    backgroundColor: '#faf8ff',
    frame: false,
    autoHideMenuBar: true,
    webPreferences: {
      preload: path.join(__dirname, 'preload.mjs'),
      nodeIntegration: false,
      contextIsolation: true,
    },
  });

  // Hide menu bar for cleaner look
  mainWindow.setMenuBarVisibility(false);
  mainWindow.setMenu(null);

  // vite-plugin-electron sets process.env.VITE_DEV_SERVER_URL during dev
  if (process.env.VITE_DEV_SERVER_URL) {
    mainWindow.loadURL(process.env.VITE_DEV_SERVER_URL)
    mainWindow.webContents.openDevTools()
  } else {
    // In production, the built React app is in the dist folder
    mainWindow.loadFile(path.join(__dirname, '../dist/index.html'))
  }
}

app.whenReady().then(() => {
  startBackend()
  createWindow()

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow()
    }
  })

  ipcMain.on('window-minimize', () => {
    mainWindow?.minimize()
  })

  ipcMain.on('window-maximize', () => {
    if (!mainWindow) return
    if (mainWindow.isMaximized()) {
      mainWindow.unmaximize()
    } else {
      mainWindow.maximize()
    }
  })

  ipcMain.on('window-close', () => {
    mainWindow?.close()
  })
})

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit()
  }
})

app.on('quit', () => {
  if (backendProcess) {
    backendProcess.kill()
  }
})