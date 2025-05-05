"use client"

import { useState, useEffect } from "react"
import { motion } from "framer-motion"
import { Slider } from "@/components/ui/slider"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { ArrowDown, Moon, Sun } from 'lucide-react'
import { Button } from "@/components/ui/button"
import { useTheme } from "next-themes"

export default function CaesarCipher() {
  const [shift, setShift] = useState(3)
  const [text, setText] = useState("HELLO WORLD")
  const [mounted, setMounted] = useState(false)
  const { theme, setTheme } = useTheme()

  // Handle mounting for theme
  useEffect(() => {
    setMounted(true)
  }, [])

  const alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".split("")

  // Encrypt text using Caesar cipher
  const encrypt = (text: string, shift: number) => {
    return text
      .toUpperCase()
      .split("")
      .map((char) => {
        if (char === " ") return " "
        const index = alphabet.indexOf(char)
        if (index === -1) return char
        const newIndex = (index + shift) % 26
        return alphabet[newIndex]
      })
      .join("")
  }

  if (!mounted) {
    return null
  }

  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-gray-50 dark:bg-gray-950 p-4 text-gray-900 dark:text-white">
      <motion.div 
        className="w-full max-w-6xl space-y-8 rounded-xl bg-white dark:bg-gray-900 p-8 shadow-lg"
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ 
          type: "spring", 
          stiffness: 260, 
          damping: 20, 
          duration: 0.5 
        }}
      >
        <div className="flex justify-between items-center">
          <h1 className="text-3xl font-bold">Caesar Cipher Visualization</h1>
          <Button
            variant="outline"
            size="icon"
            onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
            className="ml-auto"
          >
            {theme === "dark" ? <Sun className="h-5 w-5" /> : <Moon className="h-5 w-5" />}
            <span className="sr-only">Toggle theme</span>
          </Button>
        </div>

        <div className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="text-input">Enter text to encrypt:</Label>
            <Input
              id="text-input"
              value={text}
              onChange={(e) => setText(e.target.value)}
              className="font-mono text-lg dark:bg-gray-800 dark:border-gray-700"
              placeholder="Enter text to encrypt"
            />
          </div>

          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <Label>Shift key: {shift}</Label>
            </div>
            <Slider
              value={[shift]}
              min={0}
              max={25}
              step={1}
              onValueChange={(value) => setShift(value[0])}
              className="py-4"
            />
          </div>
        </div>

        <div className="mt-8 space-y-6">
          <div className="flex flex-col items-center">
            <div className="text-center text-sm font-medium text-gray-500 dark:text-gray-400 mb-2">
              Original Alphabet
            </div>
            <StaticCipherTable shift={shift} text={text} />
          </div>

          <div className="mt-8 grid grid-cols-1 gap-4 md:grid-cols-2">
            <div className="rounded-lg bg-gray-100 dark:bg-gray-800 p-6">
              <h3 className="mb-2 font-semibold">Original Text:</h3>
              <p className="font-mono text-lg">{text}</p>
            </div>
            <div className="rounded-lg bg-gray-100 dark:bg-gray-800 p-6">
              <h3 className="mb-2 font-semibold">Encrypted Text:</h3>
              <p className="font-mono text-lg">{encrypt(text, shift)}</p>
            </div>
          </div>

          <div className="rounded-lg bg-gray-100 dark:bg-gray-800 p-6">
            <h3 className="mb-2 font-semibold">How it works:</h3>
            <p className="text-gray-700 dark:text-gray-300">
              The Caesar cipher shifts each letter in the plaintext by a fixed number of positions in the alphabet. For
              example, with a shift of 3, A becomes D, B becomes E, and so on. The top row shows the original alphabet,
              while the bottom row shows the shifted alphabet.
            </p>
          </div>
        </div>
      </motion.div>
    </div>
  )
}

interface CipherTableProps {
  shift: number
  text: string
}

function StaticCipherTable({ shift, text }: CipherTableProps) {
  const alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".split("")
  const cellWidth = 36
  const cellHeight = 50
  const cellSpacing = 2

  // Get unique letters from the input text (excluding spaces)
  const uniqueLetters = [
    ...new Set(
      text
        .toUpperCase()
        .split("")
        .filter((char) => char !== " "),
    ),
  ]

  // Create a map of letters that should have arrows
  const arrowMap = uniqueLetters.reduce(
    (acc, letter) => {
      const index = alphabet.indexOf(letter)
      if (index !== -1) {
        acc[letter] = true
      }
      return acc
    },
    {} as Record<string, boolean>,
  )

  // Create shifted alphabet
  const shiftedAlphabet = [...alphabet.slice(shift), ...alphabet.slice(0, shift)]

  return (
    <motion.div 
      className="flex flex-col items-center w-full overflow-x-auto"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.3, duration: 0.5 }}
    >
      {/* Original alphabet row */}
      <div className="flex mb-1">
        {alphabet.map((letter) => (
          <div
            key={`original-${letter}`}
            className="flex items-center justify-center border border-gray-300 dark:border-gray-700 bg-gray-100 dark:bg-gray-800"
            style={{
              width: `${cellWidth}px`,
              height: `${cellHeight}px`,
              margin: `0 ${cellSpacing / 2}px`,
            }}
          >
            <span className="text-lg font-bold">{letter}</span>
          </div>
        ))}
      </div>

      {/* Arrow indicators - positioned correctly under each letter */}
      <div className="flex h-6">
        {alphabet.map((letter) => (
          <div
            key={`arrow-${letter}`}
            className="flex items-center justify-center"
            style={{
              width: `${cellWidth + cellSpacing}px`,
            }}
          >
            {arrowMap[letter] && <ArrowDown className="h-5 w-5 text-blue-500 dark:text-blue-400" />}
          </div>
        ))}
      </div>

      {/* Shifted alphabet row - static representation */}
      <div className="flex">
        {shiftedAlphabet.map((letter) => (
          <div
            key={`shifted-${letter}`}
            className="flex items-center justify-center border border-gray-300 dark:border-gray-700 bg-gray-100 dark:bg-gray-800"
            style={{
              width: `${cellWidth}px`,
              height: `${cellHeight}px`,
              margin: `0 ${cellSpacing / 2}px`,
            }}
          >
            <span className="text-lg font-bold">{letter}</span>
          </div>
        ))}
      </div>

      <div className="mt-2 text-center text-sm font-medium text-gray-500 dark:text-gray-400">
        Shifted Alphabet (Shift: {shift})
      </div>
    </motion.div>
  )
}
