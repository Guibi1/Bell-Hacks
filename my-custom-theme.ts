import { CustomThemeConfig } from "@skeletonlabs/tw-plugin"


export const myCustomTheme: CustomThemeConfig = {
    name: 'my-custom-theme',
    properties: {
		// =~= Theme Properties =~=
		"--theme-font-family-base": `Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, 'Noto Sans', sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol', 'Noto Color Emoji'`,
		"--theme-font-family-heading": `Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, 'Noto Sans', sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol', 'Noto Color Emoji'`,
		"--theme-font-color-base": "0 0 0 0",
		"--theme-font-color-dark": "255 255 255",
		"--theme-rounded-base": "8px",
		"--theme-rounded-container": "24px",
		"--theme-border-base": "4px",
		// =~= Theme On-X Colors =~=
		"--on-primary": "0 0 0",
		"--on-secondary": "255 255 255",
		"--on-tertiary": "255 255 255",
		"--on-success": "0 0 0",
		"--on-warning": "0 0 0",
		"--on-error": "0 0 0",
		"--on-surface": "0 0 0",
		// =~= Theme Colors  =~=
		// primary | #add5dc 
		"--color-primary-50": "243 249 250", // #f3f9fa
		"--color-primary-100": "239 247 248", // #eff7f8
		"--color-primary-200": "235 245 246", // #ebf5f6
		"--color-primary-300": "222 238 241", // #deeef1
		"--color-primary-400": "198 226 231", // #c6e2e7
		"--color-primary-500": "173 213 220", // #add5dc
		"--color-primary-600": "156 192 198", // #9cc0c6
		"--color-primary-700": "130 160 165", // #82a0a5
		"--color-primary-800": "104 128 132", // #688084
		"--color-primary-900": "85 104 108", // #55686c
		// secondary | #5692aa 
		"--color-secondary-50": "230 239 242", // #e6eff2
		"--color-secondary-100": "221 233 238", // #dde9ee
		"--color-secondary-200": "213 228 234", // #d5e4ea
		"--color-secondary-300": "187 211 221", // #bbd3dd
		"--color-secondary-400": "137 179 196", // #89b3c4
		"--color-secondary-500": "86 146 170", // #5692aa
		"--color-secondary-600": "77 131 153", // #4d8399
		"--color-secondary-700": "65 110 128", // #416e80
		"--color-secondary-800": "52 88 102", // #345866
		"--color-secondary-900": "42 72 83", // #2a4853
		// tertiary | #0c1129 
		"--color-tertiary-50": "219 219 223", // #dbdbdf
		"--color-tertiary-100": "206 207 212", // #cecfd4
		"--color-tertiary-200": "194 196 202", // #c2c4ca
		"--color-tertiary-300": "158 160 169", // #9ea0a9
		"--color-tertiary-400": "85 88 105", // #555869
		"--color-tertiary-500": "12 17 41", // #0c1129
		"--color-tertiary-600": "11 15 37", // #0b0f25
		"--color-tertiary-700": "9 13 31", // #090d1f
		"--color-tertiary-800": "7 10 25", // #070a19
		"--color-tertiary-900": "6 8 20", // #060814
		// success | #b8ff4d 
		"--color-success-50": "244 255 228", // #f4ffe4
		"--color-success-100": "241 255 219", // #f1ffdb
		"--color-success-200": "237 255 211", // #edffd3
		"--color-success-300": "227 255 184", // #e3ffb8
		"--color-success-400": "205 255 130", // #cdff82
		"--color-success-500": "184 255 77", // #b8ff4d
		"--color-success-600": "166 230 69", // #a6e645
		"--color-success-700": "138 191 58", // #8abf3a
		"--color-success-800": "110 153 46", // #6e992e
		"--color-success-900": "90 125 38", // #5a7d26
		// warning | #ffb066 
		"--color-warning-50": "255 243 232", // #fff3e8
		"--color-warning-100": "255 239 224", // #ffefe0
		"--color-warning-200": "255 235 217", // #ffebd9
		"--color-warning-300": "255 223 194", // #ffdfc2
		"--color-warning-400": "255 200 148", // #ffc894
		"--color-warning-500": "255 176 102", // #ffb066
		"--color-warning-600": "230 158 92", // #e69e5c
		"--color-warning-700": "191 132 77", // #bf844d
		"--color-warning-800": "153 106 61", // #996a3d
		"--color-warning-900": "125 86 50", // #7d5632
		// error | #ff7a7a 
		"--color-error-50": "255 235 235", // #ffebeb
		"--color-error-100": "255 228 228", // #ffe4e4
		"--color-error-200": "255 222 222", // #ffdede
		"--color-error-300": "255 202 202", // #ffcaca
		"--color-error-400": "255 162 162", // #ffa2a2
		"--color-error-500": "255 122 122", // #ff7a7a
		"--color-error-600": "230 110 110", // #e66e6e
		"--color-error-700": "191 92 92", // #bf5c5c
		"--color-error-800": "153 73 73", // #994949
		"--color-error-900": "125 60 60", // #7d3c3c
		// surface | #fcfaeb 
		"--color-surface-50": "255 254 252", // #fffefc
		"--color-surface-100": "254 254 251", // #fefefb
		"--color-surface-200": "254 254 250", // #fefefa
		"--color-surface-300": "254 253 247", // #fefdf7
		"--color-surface-400": "156 192 198", // #fdfcf1
		"--color-surface-500": "173,213,220", // #fcfaeb
		"--color-surface-600": "227 225 212", // #e3e1d4
		"--color-surface-700": "189 188 176", // #bdbcb0
		"--color-surface-800": "151 150 141", // #97968d
		"--color-surface-900": "123 123 115", // #7b7b73
		
	}
}
